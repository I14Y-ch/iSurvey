import requests
from lxml import etree
import logging

'''
These codelists have been identified to cause a speicific SQL-Error (by manual uploading)
and will not use the value as the code like in I14y, but will use a generated code instead (L0001, L0002, ...).
The reason is not clear yet, and they were added to the list as a temporary solution
'''
SQL_LABEL_ID_ERROR_LIST = ['Zahlung der Leistung',
                           'Regime der sozialen Sicherheit in der Schweiz',
                           'Regime der sozialen Sicherheit',
                           'Gegengebiet',
                           'Detaillierte Sozialleistung',
                           'DocumentEntry.languageCode',
                           'EprPurposeOfUse',
                           'Art der Ausgabe',
                           'Funktion des Sozialschutzes',
                           'Gruppierung von Ländern in Europa für GRSS',
                           'Bedürftigkeitsprüfung',
                           'NOGA OFS50',
                           'Art der Rente',
                           'Art der Einnahme',
                           'Hauptarten von Einnahmen',
                           'EU Themenvokabular',
                           'Aktualisierungsintervall',
                           'I14Y Vertraulichkeit Personendaten']


def download_i14y_data():
    logging.info('Downloading i14y data codelists...')
    url = 'https://input.i14y.admin.ch/api/ConceptSummary/search?page=0&pageSize=1000'
    data = requests.get(url).json()

    code_lists = []
    codes = [(entry['id'], entry['identifier'], entry['name']) for entry in data if entry['conceptType'] == 'CodeList']

    for id, identifier, name in codes:
        url = f'https://input.i14y.admin.ch/api/ConceptInput/{id}/codelistEntries?page=1&pageSize=10000'
        response = requests.get(url)
        if response.status_code == 200:
            code_lists.append({'id': id, 'identifier': identifier, 'name': name, 'codelist': response.json()})

    # save_file = open("codelists.json", "w")
    # json.dump(codelists, save_file, indent = 6)
    # save_file.close()

    return code_lists


def generate_limesurvey_labelset(codelists, filename="isurvey_codelist.lsl"):
    if len(codelists) == 1:
        filename = f'lsl-files/{codelists[0]["identifier"]}.lsl'
    logging.info(f'Generating LimeSurvey labelset {filename}...')
    document = etree.Element('document')
    etree.SubElement(document, 'LimeSurveyDocType').text = 'Label set'
    etree.SubElement(document, 'DBVersion').text = '623'

    labelsets = etree.SubElement(document, 'labelsets')
    fields_ls = etree.SubElement(labelsets, 'fields')
    for fname in ['lid', 'owner_id', 'label_name', 'languages']:
        etree.SubElement(fields_ls, 'fieldname').text = fname
    rows_ls = etree.SubElement(labelsets, 'rows')

    labels = etree.SubElement(document, 'labels')
    fields_lbl = etree.SubElement(labels, 'fields')
    for fname in ['id', 'lid', 'code', 'sortorder', 'assessment_value']:
        etree.SubElement(fields_lbl, 'fieldname').text = fname
    rows_lbl = etree.SubElement(labels, 'rows')

    label_l10ns = etree.SubElement(document, 'label_l10ns')
    fields_l10n = etree.SubElement(label_l10ns, 'fields')
    for fname in ['id', 'label_id', 'title', 'language']:
        etree.SubElement(fields_l10n, 'fieldname').text = fname
    rows_l10n = etree.SubElement(label_l10ns, 'rows')

    lid = 1
    code_id = 1
    lang_id = 1

    for codelist in codelists:
        if not len(codelists) == 1 and (len(codelist['codelist']) < 2 or len(codelist['codelist']) > 1000):
            logging.warning(
                f'Code list {codelist["name"]["de"]} has just one entry or more than 1000 entries, skipping...')
            continue
        row_ls = etree.SubElement(rows_ls, 'row')
        etree.SubElement(row_ls, 'lid').text = etree.CDATA(str(lid))
        etree.SubElement(row_ls, 'owner_id').text = etree.CDATA("1")
        etree.SubElement(row_ls, 'label_name').text = etree.CDATA(codelist['name']['de'])
        # Take only the languages that are in the codelist and not None
        languages = []
        for entry in codelist['codelist']:
            for lang in entry['name']:
                if 'name' in entry and entry['name'][lang] is not None and lang not in languages:
                    languages.append(lang)

        etree.SubElement(row_ls, 'languages').text = etree.CDATA(' '.join(languages))

        too_long = False
        # If any of codelist['codelist']['value'] is longer than 20 chars
        for entry in codelist['codelist']:
            if len(entry['value']) > 20:
                logging.warning(
                    f'Code list {codelist["name"]["de"]} has a value {entry["value"]} longer than 20 chars, skipping...')
                too_long = True
                break

        list_id = 1
        for code in codelist['codelist']:
            row_lbl = etree.SubElement(rows_lbl, 'row')
            etree.SubElement(row_lbl, 'id').text = etree.CDATA(str(code_id))
            etree.SubElement(row_lbl, 'lid').text = etree.CDATA(str(lid))
            if too_long or codelist["name"]["de"] in SQL_LABEL_ID_ERROR_LIST:
                etree.SubElement(row_lbl, 'code').text = etree.CDATA(f'L{str(list_id).zfill(4)}')
            else:
                etree.SubElement(row_lbl, 'code').text = etree.CDATA(code['value'])
            etree.SubElement(row_lbl, 'sortorder').text = etree.CDATA(
                str(code_id))  # Assuming sortorder is the same as the id
            etree.SubElement(row_lbl, 'assessment_value').text = etree.CDATA("0")  # Assuming 0 as the assessment value

            for lang in languages:
                row_l10n = etree.SubElement(rows_l10n, 'row')
                etree.SubElement(row_l10n, 'id').text = etree.CDATA(str(lang_id))
                etree.SubElement(row_l10n, 'label_id').text = etree.CDATA(str(code_id))
                if code['name'][lang] is None:
                    etree.SubElement(row_l10n, 'title').text = etree.CDATA('')
                else:
                    etree.SubElement(row_l10n, 'title').text = etree.CDATA(code['name'][lang])
                etree.SubElement(row_l10n, 'language').text = etree.CDATA(lang)

                lang_id += 1

            code_id += 1
            list_id += 1

        lid += 1

    tree = etree.ElementTree(document)
    tree.write(filename, pretty_print=True, encoding='UTF-8', xml_declaration=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    codelists = download_i14y_data()
    for codelist in codelists:
        codelist['name']['roh'] = codelist['name'].pop('rm')
        for code in codelist['codelist']:
            code['name']['roh'] = code['name'].pop('rm')

    logging.info('Generating LimeSurvey labelset with all codelists...')
    generate_limesurvey_labelset(codelists)

    logging.info('Generating LimeSurvey labelset with each codelist...')
    for i in range(0, len(codelists)):
        logging.info(f'Processing codelist on postion {i}')
        generate_limesurvey_labelset([codelists[i]])

    logging.info('Done!')

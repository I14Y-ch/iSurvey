import requests
from lxml import etree
import logging

def download_i14y_data():
    logging.info('Downloading i14y data codelists...')
    url = 'https://input.i14y.admin.ch/api/ConceptSummary/search?page=0&pageSize=1000'
    data = requests.get(url).json()

    code_lists = []
    codes = [(entry['id'], entry['name']) for entry in data if entry['conceptType'] == 'CodeList']

    for id, name in codes:
        url = f'https://input.i14y.admin.ch/api/ConceptInput/{id}/codelistEntries?page=1&pageSize=10000'
        response = requests.get(url)
        if response.status_code == 200:
            code_lists.append({'id': id, 'name': name, 'codelist': response.json()})

    # save_file = open("codelists.json", "w")
    # json.dump(codelists, save_file, indent = 6)
    # save_file.close()

    return code_lists


def generate_limesurvey_labelset(codelists, filename="./i14y/app/isurvey_codelist.lsl"):
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
        if len(codelist['codelist']) > 1000:
            logging.warning(f'Code list {codelist["name"]["de"]} has more than 1000 entries, skipping...')
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

        list_id = 1
        for code in codelist['codelist']:
            row_lbl = etree.SubElement(rows_lbl, 'row')
            etree.SubElement(row_lbl, 'id').text = etree.CDATA(str(code_id))
            etree.SubElement(row_lbl, 'lid').text = etree.CDATA(str(lid))
            etree.SubElement(row_lbl, 'code').text = etree.CDATA(f'L{str(list_id).zfill(4)}')
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

    generate_limesurvey_labelset(codelists)
    logging.info('Job successful')

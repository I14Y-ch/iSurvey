import requests
from lxml import etree
import logging
import json

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

    save_file = open("codelists.json", "w")
    json.dump(code_lists, save_file, indent = 6)
    save_file.close()

    return code_lists


def test_special_character(codelist, spec_char):
    vals = []
    for code in codelist:
        vals.append(code['value'])

    for val in vals:
        if spec_char in val:
            return True
        
    return False

def test_code_length(codelist, length):
    vals = []
    for code in codelist:
        vals.append(code['value'])

    for val in vals:
        if len(str(val)) > length:
            return True
        
    return False
            


def generate_limesurvey_labelset(codelists, filename="isurvey_codelist.lsl", blacklist=[]):
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
    exclusions = []

    for codelist in codelists:
        if codelist['name']['de'] in blacklist:
            exclusions.append(codelist['name']['de'])
            print('Skip', codelist['name']['de'])
            continue

        if test_special_character(codelist['codelist'], '_'):
            exclusions.append(codelist['name']['de'])
            print('Skip', codelist['name']['de'])
            continue

        if test_code_length(codelist['codelist'], 5):
            exclusions.append(codelist['name']['de'])
            print('Skip', codelist['name']['de'])
            continue
    

        if len(codelist['codelist']) >= 100:
            logging.info(f'Codelist {codelist["name"]} has more than 1000 entries, skipping...')
            exclusions.append(codelist['name']['de'])
            print('Skip', codelist['name']['de'])
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
            etree.SubElement(row_lbl, 'code').text = etree.CDATA('code_'+code['value'])
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

    with open(r'exclusions.txt', 'w') as fp:
        for item in exclusions:
            # write each item on a new line
            fp.write("%s\n" % item)

    print(exclusions)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # codelists = download_i14y_data()
    with open('codelists.json', 'r') as file:
        codelists = json.load(file)

    blacklist = [
        'I14Y Vertraulichkeit Personendaten',
        'Beziehung zwischen Datasets'
    ]



    for codelist in codelists:
        codelist['name']['roh'] = codelist['name'].pop('rm')
        for code in codelist['codelist']:
            code['name']['roh'] = code['name'].pop('rm')

    generate_limesurvey_labelset(codelists, blacklist=blacklist)
    logging.info('Job successful')
    quit()

    size = 1
    for i in range(0, len(codelists), size):
        logging.info(f'Processing codelists {i} to {i + size}')
        generate_limesurvey_labelset(codelists[i:i + size], f'lsl-files/isurvey_codelist_{i}.lsl')

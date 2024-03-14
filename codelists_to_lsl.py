import requests


def download_i14y_data():
    url = 'https://input.i14y.admin.ch/api/ConceptSummary/search?page=0&pageSize=1000'
    data = requests.get(url).json()

    codelists = []
    codes = [(entry['id'], entry['name']) for entry in data if entry['conceptType'] == 'CodeList']

    for id, name in codes:
        url = f'https://input.i14y.admin.ch/api/ConceptInput/{id}/codelistEntries?page=1&pageSize=10000'
        response = requests.get(url)
        if response.status_code == 200:
            codelists.append({'id': id, 'name': name, 'codelist': response.json()})

    # save_file = open("codelists.json", "w")
    # json.dump(codelists, save_file, indent = 6)
    # save_file.close()

    return codelists


def generate_isurvey_codelist(codelists):
    document = '''
        <?xml version="1.0" encoding="UTF-8"?>
        <document>
        <LimeSurveyDocType>Label set</LimeSurveyDocType>
        <DBVersion>623</DBVersion>
        '''

    labelsets = '''
    <labelsets>
    <fields>
    <fieldname>lid</fieldname>
    <fieldname>label_name</fieldname>
    <fieldname>languages</fieldname>
    </fields>
    <rows>
    '''

    labels = '''
    <labels>
    <fields>
    <fieldname>id</fieldname>
    <fieldname>lid</fieldname>
    <fieldname>code</fieldname>
    <fieldname>sortorder</fieldname>
    </fields>
    <rows>
    '''

    label_l10ns = '''
    <label_l10ns>
    <fields>
    <fieldname>id</fieldname>
    <fieldname>label_id</fieldname>
    <fieldname>title</fieldname>
    <fieldname>language</fieldname>
    </fields>
    <rows>
    '''

    lid = 1
    code_id = 1
    lang_id = 1
    languages = ['de', 'en', 'fr', 'it']

    for entry in codelists:

        labelsets += f''' 
            <row>
                <lid><![CDATA[{lid}]]></lid>
                <label_name><![CDATA[{entry['name']['de']}]]></label_name>
                <languages><![CDATA[de en fr it]]></languages>
            </row>
        '''
        for code in entry['codelist']:
            labels += f'''
            <row>
                <id><![CDATA[{code_id}]]></id>
                <lid><![CDATA[{lid}]]></lid>
                <code><![CDATA[{code['value']}]]></code>
                <sortorder><![CDATA[{code_id}]]></sortorder>
            </row>
            '''

            for i in range(len(languages)):
                label_l10ns += f'''
                    <row>
                        <id><![CDATA[{lang_id}]]></id>
                        <label_id><![CDATA[{code_id}]]></label_id>
                        <title><![CDATA[{code['name'][languages[i]]}]]></title>
                        <language><![CDATA[[{languages[i]}]]></language>
                    </row>
                '''

                lang_id += 1

            code_id += 1

        lid += 1

    labelsets += '''
    </rows>
    </labelsets
    '''

    labels += '''
    </rows>
    </labels>
    '''

    label_l10ns += '''
    </rows>
    </label_l10ns>
    '''

    document = labelsets + labels + label_l10ns

    return document


if __name__ == "__main__":
    codelists = download_i14y_data()
    xml = generate_isurvey_codelist(codelists[:2])
    # Write xml to file
    with open('codelists.lsl', 'w') as file:
        file.write(xml)
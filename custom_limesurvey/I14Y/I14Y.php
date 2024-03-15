<?php
Yii::import('application.helpers.admin.import_helper', true);

class I14Y extends PluginBase {
	static protected $description = "Download I14Y Named Sets to LimeSurvey";
	static protected $name = "I14Y";
	protected $storage  = 'DbStorage';
	protected $settings = array(
		'i14yURI' => array(
			'type' => 'string',
			'label' => 'Download-URL für I14Y-Daten',
			'default' => 'https://raw.githubusercontent.com/I14Y-ch/iSurvey/main/i14y/app/isurvey_codelist.lsl'
		)
	);
	public function init() {
		$this->subscribe('afterPluginLoad');
	}
	public function afterPluginLoad() {
		if (!$this->getEvent()) {
			throw new CHttpException(403);
		}
		if (Yii::app() instanceof CConsoleApplication) {
			return;
		}
		$this->downloadI14Y();
	}
	private function downloadI14Y() {
		$options = array(
			'checkforduplicates' => 'on'
		);
		$url = $this->getPluginSettings()['i14yURI']['current'];
		$this->log($url);
		$tmpfile = tempnam(sys_get_temp_dir(), 'i14y');
		$this->log("Processing download ...");
		// Download contents of URL to temporary file

		// Parse and import results to Limesurvey API
		$importResults = XMLImportLabelsets($tmpfile, $options); // https://api.limesurvey.org/namespaces/default.html#function_XMLImportLabelsets
		$this->log($importResults);
	}
}
?>

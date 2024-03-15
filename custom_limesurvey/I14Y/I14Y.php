<?php
Yii::import('application.helpers.admin.import_helper', true);

class I14Y extends PluginBase {
	protected static $description = "Download I14Y Named Sets to LimeSurvey";
	protected static $name = "I14Y";
	protected $storage  = 'DbStorage';
	protected $settings = array(
		'i14yURI' => array(
			'type' => 'string',
			'label' => 'Download-URL für I14Y-Daten',
			'default' => 'https://raw.githubusercontent.com/I14Y-ch/iSurvey/main/i14y/app/isurvey_codelist.lsl'
		),
        'lastCheck' => array(
            'type' => 'date',
            'label' => 'Letzter Update Versuch'
         ),
         'lastCheckSuccessful' => array(
             'type' => 'boolean',
             'label' => 'Letztes Update erfolgreich'
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
        $this->log('Import start');
	    $importResults = null;
	    $lastCheck = $this->getPluginSettings()['lastCheck']['current'];
	    $dateDiff = 0;
	    $now = new DateTime();
	    if ($lastCheck != null) {
	        $this->log('Last Check ' . $lastCheck);
	        $parsedDate = DateTime::createFromFormat('d.m.Y H:i', $lastCheck);
	        $dateDiff = date_diff($now, $parsedDate)->d;
	    }
        $this->log('Last Check ' . $lastCheck);
        $this->log('Date Diff ' . $dateDiff);
        $this->set('lastCheckSuccessful', false);
        $this->set('lastCheck', $now->format('d.m.Y H:i'));
	    if ($lastCheck == null || $dateDiff >= 1) {
            $options = array(
                'checkforduplicates' => 'off'
            );
            $url = $this->getPluginSettings()['i14yURI']['current'];
            $this->log('URL ' . $url);
            $tmpfile = tempnam(sys_get_temp_dir(), 'i14y');
            $this->log("Processing download ...");
            try {
                // Download contents of URL to temporary file
                $this->downloadFile($url, $tmpfile);
                // Parse and import results to Limesurvey API
                $importResults = XMLImportLabelsets($tmpfile, $options); // https://api.limesurvey.org/namespaces/default.html#function_XMLImportLabelsets
            } catch (Exception $e) {
                $importResults = $e->getMessage();
            }
            $this->log($importResults);
        }
        $this->set('lastCheckSuccessful', empty($importResults));
        $this->log('imported');
	}
	private function downloadFile($url, $tmpfile) {
	    set_time_limit(0);

         $file = fopen($tmpfile, 'w+');

         $curl = curl_init();

         curl_setopt_array($curl, [
             CURLOPT_URL            => $url,
             CURLOPT_RETURNTRANSFER => 1,
             CURLOPT_FILE           => $file,
             CURLOPT_TIMEOUT        => 50,
             CURLOPT_USERAGENT      => 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)'
         ]);

         $response = curl_exec($curl);

         if($response === false) {
             throw new \Exception('Curl error: ' . curl_error($curl));
         }
         $this->log($response);
         $response;
	}
}
?>

<?php
class crawler
{
    protected $url;
    protected $path = 'D:/codeCamp/';

    public function getContent($url)
    {
        $handle = @curl_init();
        curl_setopt($handle, CURLOPT_URL, $url);
        $head[] = "Connection: keep-alive";
        $head[] = "Keep-Alive: 300";
        $head[] = "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7";
        $head[] = "Accept-Language: en-us,en;q=0.5";
        curl_setopt($handle, CURLOPT_USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)  Chrome/68.0.3440.84 Safari/537.36');
        curl_setopt($handle, CURLOPT_ENCODING, '');
        curl_setopt($handle, CURLOPT_HTTPHEADER, $head);
        curl_setopt($handle, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($handle, CURLOPT_SSL_VERIFYHOST, FALSE);
        curl_setopt($handle, CURLOPT_SSL_VERIFYPEER, FALSE);
        curl_setopt($handle, CURLOPT_TIMEOUT, 60);
        curl_setopt($handle, CURLOPT_CONNECTTIMEOUT, 60);
        curl_setopt($handle, CURLOPT_FOLLOWLOCATION, TRUE);
        curl_setopt($handle, CURLOPT_HTTPHEADER, array( 'Expect:' ));
        $contents = curl_exec($handle);
        curl_close($handle);
        return $contents;
    }

    # fetch URLs from html and return array
    public function getCSS($url)
    {
        $contents = $this->getContent($url);

        preg_match_all('/<link\s+(?:[^>]*?\s+)?href="([^"]*)"/', $contents, $rawLinks);

        return $rawLinks[1];
    }

# fetch URLs from html and return array
    public function getJS($url)
    {
        $contents = $this->getContent($url);

        preg_match_all('/<script\s+(?:[^>]*?\s+)?src="([^"]*)"/', $contents, $rawLinks);

        return $rawLinks[1];
    }

    public function getTemplate($url)
    {
        mkdir($this->path . '/files');
        chmod($this->path . '/files', 0777);
        $html_data = $this->getContent($url);
        $templateLinks = array_merge($this -> getCSS($url), $this->getJS($url));


        foreach ($templateLinks as $templateLink) {

            if (strpos($templateLink, '.css') !== false || strpos($templateLink, '.js') !== false) {

                if ($this->has_prefix($templateLink, 'http')) {
                    $content = $this->getContent($templateLink);
                } else {
                    $content = $this->getContent($url.$templateLink);
                }

                $filename = 'files/' . end(explode('/', $templateLink));
// Replace text in html file
                $html_data = str_replace($templateLink, $filename, $html_data);

                $filePath = $this->path . $filename;
                $file = fopen($filePath, "w") or die("Unable to open file!");
                fwrite($file, $content);
                fclose($file);
                chmod($filePath, 0777);
            }

        }

// Save html file
        $file = fopen($this->path . 'index.html', "w") or die("Unable to open file!");
        fwrite($file, $html_data);
        fclose($file);
        chmod($this->path . 'index.html', 0777);
        echo "Done!";
    }

    function has_prefix($string, $prefix)
    {
        return ((substr($string, 0, strlen($prefix)) == $prefix) ? true : false);
    }

}

$crawler = new crawler();
$crawler->getTemplate('https://v4-alpha.getbootstrap.com/');
//$link ->getTemplate();

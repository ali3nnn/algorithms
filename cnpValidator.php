<?php

function cnpValidator($cnp) {
    $len = checkLength($cnp);
    // echo 'Length is '.($len ? '':'not ').'valid <br>';

    $lastDigit = checkLastDigit($cnp);
    // echo 'Last digit is '.($lastDigit ? '':'not ').'valid <br>';

    $birth = checkBirth($cnp);
    // echo 'Birth is '.($birth ? '':'not ').'valid <br>';

    $county = checkCounty($cnp);
    // echo 'County is '.($county ? '':'not ').'valid <br>';
   
    // echo 'CNP is '.(($len and $lastDigit and $birth and $county) ? '':'not ').'valid <br>';

    return $len and $lastDigit and $birth and $county;

}

function checkLength($cnp) {
    if(strlen($cnp) != 13) {
        return false;
    } else {
        return true;
    }
}

function checkLastDigit($cnp) {
    
    $calc = array(2,7,9,1,4,6,3,5,8,2,7,9);
    $sum = 0;
    $raw_cnp = str_split($cnp);
    $lastDigit = 0;
    
    for($n=0 ; $n<13 ; $n++) {
        
        if(!is_numeric($cnp[$n])) {
            return false;
        }
        
        $cnp[$n] = intval($cnp[$n]);
        
        if($n < 12) {
            $sum += $cnp[$n] * $calc[$n];
        } else {
            $lastDigit = $cnp[$n];
        }
    }
    
    $res = $sum % intval('11');
    
    if($res==10 && $lastDigit == 1) {
        return true;
    } elseif($res == $lastDigit) {
        return true;
    } else {
        return false;
    }
    
}

function checkBirth($cnp) {
    $raw_cnp = str_split($cnp);

    // check year < current_year
    $year = $raw_cnp[1].$raw_cnp[2];
    $year = intval($year);
    switch( intval($raw_cnp[0]) ) {
        case 1  : case 2 : { $year += 1900; } break; 
        case 3  : case 4 : { $year += 1800; } break; 
        case 5  : case 6 : { $year += 2000; } break;
        case 7  : case 8 : case 9 : { $year += 2000;} break;
        default : { return false; } break;
    }
    $yearBool = $year <= date("Y");

    // check month < 12
    $month = $raw_cnp[3].$raw_cnp[4];
    $month = intval($month);
    $monthBool = $month <= 12;

    // check month < current month if current_year
    if($year == date("Y")) {
        if($month > date('m')) {
            $monthBool = false;
        }
    }

    // check day < days of month
    $day = $raw_cnp[5].$raw_cnp[6];
    $day = intval($day);
    $dayMax = cal_days_in_month(CAL_GREGORIAN, $month, $year);
    $dayBool = $day <= $dayMax;

    // check day < current day if current_year && current_month
    if($year == date("Y") and $month == date("m")) {
        if($day > date('d')) {
            $dayBool = false;
        }
    }

    return $dayBool and $monthBool and $yearBool;
}

function checkCounty($cnp) {
    $raw_cnp = str_split($cnp);
    $county = $raw_cnp[7].$raw_cnp[8];
    $county = intval($county);
    $county = ($county <= 46 && $county > 0) || $county == 51 || $county == 52;
    return $county;
}

// Usage
// echo "<p>CNP: ".$_POST["cnp"]."</p>";
echo (cnpValidator($_POST["cnp"])==1 ? 1 : 0);

?>


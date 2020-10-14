<?php

# Create our class
// $router = new Router;
// $router->post('/validator', function($request) {
//     $body = $request->getBody();
//     return $body;
// });

function cnpValidator($cnp) {
    $len = checkLength($cnp);

    if($len) {
        echo "<p>Length is OK</p>";
    } else {
        echo "<p>Length is not OK</p>";
    }

    $lastDigit = checkLastDigit($cnp);

    if($lastDigit) {
        echo "<p>Last digit is OK</p>";
    } else {
        echo "<p>Last digit is not OK</p>";
    }

    $birth = checkBirth($cnp);

    if($birth) {
        echo "<p>Birht date is OK</p>";
    } else {
        echo "<p>Birht date is not OK</p>";
    }

    $county = checkCounty($cnp);

    if($county) {
        echo "<p>County is OK</p>";
    } else {
        echo "<p>County is not OK</p>";
    }
}

function checkLength($cnp) {
    if(strlen($cnp) != 13) {
        return false;
    } else {
        return true;
    }
}

function checkLastDigit($cnp) {
    
    $calc = array( 2 , 7 , 9 , 1 , 4 , 6 , 3 , 5 , 8 , 2 , 7 , 9 );
    $sum = 0;
    $raw_cnp = str_split($cnp);
    $checker = 0;
    
    for($n=0 ; $n<13 ; $n++) {
        
        if(!is_numeric($cnp[$n])) {
            return false;
        }
        
        $cnp[$n] = intval($cnp[$n]);
        
        if($n < 12) {
            $sum += $cnp[$n] * $calc[$n];
        } else {
            $checker = $cnp[$n];
        }
    }
    
    $res = $sum % intval('11');
    
    if($res==10 && $checker == 1) {
        return true;
    } elseif($res == $checker) {
        return true;
    } else {
        return false;
    }
    
}

function checkBirth($cnp) {
    $raw_cnp = str_split($cnp);

    // [ ] TODO: check if year, month and day is valid date
    // [ ] TODO: check if year correspond with first digit

    $year = $raw_cnp[1].$raw_cnp[2];
    // $year = date("Y");
    $month = $raw_cnp[3].$raw_cnp[4];
    // $month = $month <= 12;
    $day = $raw_cnp[5].$raw_cnp[6];
    // $day = $day <= 31; 
    // return $year.' '.$month.' '.$day;
    return false;
}

function checkCounty($cnp) {
    // [ ] TODO: check if number for county is 1 <= x <= 52
    return false;
}



// Usage
echo "<p>CNP: ".$_POST["cnp"]."</p>";
cnpValidator($_POST["cnp"]);

?>


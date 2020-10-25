<?php

function cnpValidator($cnp) {

}

function checkLength($cnp) {
    if(strlen($cnp) != 13) {
        return 'invalid';
    }
}

function checkLastDigit($cnp) {
    
    $calc = array( 2 , 7 , 9 , 1 , 4 , 6 , 3 , 5 , 8 , 2 , 7 , 9 );
    $sum = 0;
    $raw_cnp = str_split($cnp);
    $checker = 0;
    
    for($n=0 ; $n<13 ; $n++) {
        
        if(!is_numeric($cnp[$n])) {
            return 'invalid';
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
        return 'valid';
    } elseif($res == $checker) {
        return 'valid';
    } else {
        return 'invaid';
    }
    
}



// Usage
print(cnpValidator('195090215247'));
?>


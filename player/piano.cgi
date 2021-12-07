#!/usr/bin/perl -w

use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);
use utf8;
$ufile="../resources/files/user_info.out";
$tfile="../resources/files/top_charts.out";
$sfile="../resources/files/user_profile.out";
$cfile="../resources/files/counter.out";
$delim="!---!";
$songborder="*-!-*";
$songinner="&&";
$songname=param("songname");
$songseq=param("songseq");
$uname= cookie('VP-cookie');
chomp $uname;
# user info for verification
open(IN,"<$ufile") || die "can't open $ufile for reading\n";
@lines=<IN>;
close(IN);
@temp=();
%uinfo=();
foreach $line(@lines) {
    chomp $line;
    @temp=split(/\Q$delim\E/,$line);
    $uinfo{$temp[0]}=$temp[1];
}
#----------------------------------------
#song file load
open(IN,"<$sfile") || die "can't open $sfile for reading\n";
@lines=<IN>;
close(IN);
@temp=();
%usongs=();
foreach $line(@lines) {
    chomp $line;
    if($line eq "") {
        next;
    }
    @temp=split(/\Q$delim\E/,$line);
    $usongs{$temp[0]}=$temp[1];
}
#top_charts file load
open(IN,"<$tfile") || die "can't open $tfile for reading\n";
@lines=<IN>;
close(IN);
@temp=();
%tsongs=();
foreach $line(@lines) {
    chomp $line;
    if($line eq "") {
        next;
    }
    @temp=split(/\Q$delim\E/,$line);
    $tsongs{$temp[0]}{"username"}=$temp[1];
    $tsongs{$temp[0]}{"songname"}=$temp[2];
    $tsongs{$temp[0]}{"songseq"}=$temp[3];
    $tsongs{$temp[0]}{"likes"}=$temp[4];
}
#-------------------------------------------
#if uname isn't given prompt login
if(($uname eq "")||(!exists($uinfo{$uname}))) {
print header();
    $headerphp=system '/usr/bin/php', '../landing_page/nav_land.php';
    print<<EOP;
   <html>
   <head>
    <meta charset="utf-8">
    <title>Virtual Piano</title>
    <link rel="stylesheet" href="style_message.css">
    <title>>Cookie Timed out</title>
    </head>
    <body>
    <h1 class="oops">>Cookie Timed Out</h1>
    <h2 class="type">Unfortunately the cookie couldn't be read to verify user credentials.<br></h2>
    <h3 class="obs">Please log in again</h3>
    <br><br>
    Please <a href="../user_auth/login.html">Log In</a></p>
    </body>
    </html>
EOP
exit;
}

if(($songname ne "")&&($songseq ne "")){
    open(IN,"<$cfile") || die "can't open $cfile for reading\n";
    $songid=<IN>;
    chomp $songid;
    close(IN);
    open(OUTF,">>$tfile") || die "can't open $tfile for appending\n";
    print OUTF $songid.$delim.$uname.$delim.$songname.$delim.$songseq.$delim."0\n";
    close(OUTF);
    $temp=$usongs{$uname};
    chomp $temp;
    if($temp ne "") {
        $usongs{$uname}=$temp.$songborder.$songid.$songinner.$songname.$songinner.$songseq."\n";
    }
    else {
        $usongs{$uname}=$songid.$songinner.$songname.$songinner.$songseq."\n";
    }
    open(OUTF,">$sfile") || die "Can't open $sfile for writing\n";
	foreach $key(keys %usongs) {
		print OUTF $key.$delim.$usongs{$key}."\n";
		$counter++;
	}
	close(OUTF);
    $songid++;
    open(OUTF,">$cfile") || die "can't open $cfile for reading\n";
    print OUTF "$songid\n";
    close(OUTF);
}
print header();
$headerphp=system '/usr/bin/php', '../header_footer/nav.php';
print<<EOP;
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Virtual Piano</title>
    <link rel="stylesheet" href="piano_style.css">

</head>
<body>


    <div class="band">

    <a href="drums.cgi"><button class="button" style="vertical-align:middle"><span>Drums </span></button></a>
    <a href="drums_piano.cgi"><button class="button" style="vertical-align:middle"><span>Piano+Drums </span></button></a>

    </div>

    <div class="tune">
    <form action="piano.cgi" method="post">
	    <label for="tune" class="label"><b>Tune Name:</b></label>
	    <input id="songnamein" type="text" placeholder="Name" name="songname" required>
	    <label for="tune" class="label"><b>Tunes:</b></label>
	    <input id="output" name="songseq" placeholder="Music Notes" type="text" readonly value="">
        <input type="button" value="Play" id="play">
        <input type="reset" value="Clear" id="clr">
        <input type="submit" value="Submit" id="save">
    </form>
    </div>

     

    <div class="container">
        <div class="container1 white-keys">
            <kbd>A</kbd>
            <kbd>S</kbd>
            <kbd>D</kbd>
            <kbd>F</kbd>
            <kbd>G</kbd>
            <kbd>H</kbd>
            <kbd>J</kbd>
        </div>
        <div class="black-keys">
            <kbd id="W_key">W</kbd>
            <kbd id="E_key">E</kbd>
            <kbd id="T_key">T</kbd>
            <kbd id="Y_key">Y</kbd>
            <kbd id="U_key">U</kbd>
        </div>

    </div>

<script src="PlayFunctions.js"></script>
<script src="Piano.js"></script>
</body></html> 
EOP

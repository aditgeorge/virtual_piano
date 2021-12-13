#!/usr/bin/perl -w

use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);
use utf8;
$ufile="../resources/files/user_info.out";
$tfile="../resources/files/top_charts.out";
$delim="!---!";
$songid=param("songid");
$change=param("change");
$uname= cookie('VP-cookie');
chomp $songid;
chomp $change;
chomp $uname;
open(IN,"<$ufile") || die "can't open $ufile for reading\n";
@lines=<IN>;
close(IN);
@temp=();
%uinfo=();
foreach $line(@lines) {
    chomp $line;
	if($line eq "") {
        next;
    }
    @temp=split(/\Q$delim\E/,$line);
    $uinfo{$temp[0]}{"pw"}=$temp[1];
    $uinfo{$temp[0]}{"avatar"}=$temp[2];
}
#----------------------------------------
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
#-----------------------------
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
    <h3 class="obs"><a href="../user_auth/login.html">Please click here to log in again</a></h3>
    <br><br>
    </body>
    </html>
EOP
exit;
}

if($songid ne "") {
	if($change eq "add") {
        $tsongs{$songid}{"likes"}++;
    }
    elsif($change eq "sub") {
        if($tsongs{$songid}{"likes"}!=0) {
            $tsongs{$songid}{"likes"}--;
        }
    }
	#updating the songfile
	open(OUTF,">$tfile") || die "Can't open $tfile for writing\n";
    for my $key (sort { $tsongs{$b}{"likes"} <=> $tsongs{$a}{"likes"} } keys %tsongs) {
        print OUTF $key.$delim.$tsongs{$key}{"username"}.$delim.$tsongs{$key}{"songname"}.$delim.$tsongs{$key}{"songseq"}.$delim.$tsongs{$key}{"likes"}."\n";
    }
    close(OUTF);
}
#---------------------------------
#printing to page the profile
print header();
system '/usr/bin/php', '../header_footer/nav.php';
print<<EOP;
<html>
<head>
    <title>Top Charts</title>
    <link rel="stylesheet" href="top_charts_style.css">
</head>

<!---------nav menu----------!>

<body>
	<div class="header"><h1>Top Charts</h1></div>
    <table>
    <tr class="title">
            <th width="10%">#</th>
    		<th width="10%"  style="text-align: left;Margin-left:20px">Tune</th>
    		<th  width="10%" class="col2">Creator</th>
    		<th  width="10%" class="col3">Score</th>
	</tr>
EOP
my $i=1;
for my $key (sort { $tsongs{$b}{"likes"} <=> $tsongs{$a}{"likes"} } keys %tsongs) {
    print<<EOP;
	<form action="top_charts.cgi" method="get">
		<tr>
        <td>$i</td>
        <td style="text-align: left;">
            <img class="play_icon" src="http://widit.knu.ac.kr/~adit/proj/resources/images/play_white.png" onclick="playtext('$tsongs{$key}{songseq}')">
            $tsongs{$key}{'songname'}<input type="hidden" id="songid" name="songid" value="$key">
        </td>
        <td  class="col2">
            $tsongs{$key}{'username'}
        </td>
        <td  class="col3">
            $tsongs{$key}{'likes'}&nbsp
            <button name="change" type="submit" value="add" style="background-image: url('http://widit.knu.ac.kr/~adit/proj/resources/images/thumb_up.png');background-size: cover;width: 30px;height: 30px;Margin-bottom:-10px;"></button>&nbsp
            <button name="change" type="submit" value="sub" style="background-image: url('http://widit.knu.ac.kr/~adit/proj/resources/images/thumbs_down.png');background-size: cover;width: 30px;height: 30px;Margin-bottom:-10px;"></button>
        </td>
		</tr>
        </form>
EOP
$i++;
}

print<<EOP;
	</table>
    <script src="http://widit.knu.ac.kr/~adit/proj/player/Drums_Piano.js"></script>
    <script src="http://widit.knu.ac.kr/~adit/proj/player/PlayFunctions.js"></script>
</body>

</html>
EOP
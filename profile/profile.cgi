#!/usr/bin/perl -w

use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);
use utf8;
$ufile="../resources/files/user_info.out";
$sfile="../resources/files/user_profile.out";
$songid=param("songid");
$delim="!---!";
$songborder="*-!-*";
$songinner="&&";
chomp $songid;
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
    @temp=split(/\Q$delim\E/,$line);
    $usongs{$temp[0]}=$temp[1];
}
#-----------------------------
#if uname isn't given prompt login
if(($uname eq "")||(!exists($uinfo{$uname}))) {
	print header();
print<<EOP;
<html>
<head><title>UserInfo timed out</title></head>
	
	<body style="padding:20px">
	<h2>>UserInfo timed out. Please log in again. cookie:$uname<br></h2>
	<a href="../user_auth/login.html">Log In</a>
EOP
exit;
}
#----------------------------------------
#getting specific users songs
@songs=split(/\Q$songborder\E/,$usongs{$uname});

#if deletesong param is given perform deletion
if($songid ne "") {
	$i=0;
	#searching and removing that specific song id
	foreach $song(@songs) {
		@songinfo=split(/\Q$songinner\E/,$song);
		if($songinfo[0] eq $songid) {
			last;
		}
		else {
			$i++;
		}
	}
	splice(@songs,$i,1);
	$usongs{$uname}=join($songborder,@songs);
	#updating the songfile
	open(OUTF,">$sfile") || die "Can't open $sfile for writing\n";
	foreach $key(keys %usongs) {
		print OUTF $key.$delim.$usongs{$key}."\n";
		$counter++;
	}
	close(OUTF);

}
#---------------------------------
#printing to page the profile
print header();
$headerphp=system '/usr/bin/php', '../header_footer/nav.php';
print<<EOP;
<html>
    <head>
        <link rel ="stylesheet" href="profile_style.css">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta charset="UTF-8"><title>My Profile</title>
    </head>
	
	<body style="padding:20px">
	
	<h2 style='text-align: center'>$uname's Profile</h2>
	 <div class="row">
                <div style="display: inline-block">

                    <!-- left hand side of the page -->
                    <div class="left">

                            <!-- Top Liked section -->
                            <div id="rcorners3">
                                <h3 style='text-align: center;'> $uname 's Top Tune: </h3>
                                <br>
                                <img src="no1.png" style='display:block; margin: auto;'>
                                <br>
                                <h4 style='text-align: center;'>Some Song</h4>
                                <br>
                            </div>
                    </div>

                    <!-- the right hand side of the page-->
                    <div style="display: inline-block">
                        <div style="padding:50px">

                            <!-- Music Library Display -->
                            <div id="rcorners2">
                                <nav>
                                    <h3>Music</h3>
                                    <table>
EOP
foreach $song(@songs) {
	@songinfo=split(/\Q$songinner\E/,$song);
	print<<EOP;
    <tr>
	<form action="profile.cgi" method="post">
	<input type="hidden" id="songid" name="songid" value="$songinfo[0]">
	<td>$songinfo[1]</td>
    <td>$songinfo[2]</td>
    <td><button style="float:right;"> Play </button>&nbsp<button style="float:right"> Delete </button>
    </td>
	</tr>
	</form>
EOP
}
print<<EOP;                            
                                    </ol>
                                </nav>
                            </div>

                        </div>
                    </div>

                </div>
            </div>
    </body>
</html>
EOP
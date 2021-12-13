#!/usr/bin/perl -w

use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);
use utf8;
$ufile="../resources/files/user_info.out";
$sfile="../resources/files/user_profile.out";
$tfile="../resources/files/top_charts.out";
$songid=param("songid");
$avatar=param("avatar");
$delim="!---!";
$songborder="*-!-*";
$songinner="|&&|";
chomp $songid;
chomp $avatar;
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
	if($line eq "") {
        next;
    }
    @temp=split(/\Q$delim\E/,$line);
    $uinfo{$temp[0]}{"pw"}=$temp[1];
    $uinfo{$temp[0]}{"avatar"}=$temp[2];
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
#-----------------------------
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
    <h3 class="obs"><a href="../user_auth/login.html">Please click here to log in again</a></h3>
    <br><br>
    </body>
    </html>
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
	}
	close(OUTF);
    delete($tsongs{$songid});
    open(OUTF,">$tfile") || die "Can't open $tfile for writing\n";
	foreach $key(keys %tsongs) {
		print OUTF $key.$delim.$tsongs{$key}{'username'}.$delim.$tsongs{$key}{'songname'}.$delim.$tsongs{$key}{'songseq'}.$delim.$tsongs{$key}{'likes'}."\n";
	}
	close(OUTF);

}
if($avatar ne "") {
    $uinfo{$uname}{"avatar"}=$avatar;
    open(OUTF,">$ufile") || die "Can't open $ufile for writing\n";
	foreach $key(keys %uinfo) {
		print OUTF $key.$delim.$uinfo{$key}{"pw"}.$delim.$uinfo{$key}{"avatar"}."\n";
	}
	close(OUTF);

}
$topsong="";
$toplikecount=0;
foreach $key (keys %tsongs) {
	if($tsongs{$key}{"username"} eq $uname) {
		if($topsong eq "") {
			$toplikecount=$tsongs{$key}{"likes"};
			$topsong=$tsongs{$key}{"songname"};
		}
		elsif($tsongs{$key}{"likes"} > $toplikecount) {
			$toplikecount=$tsongs{$key}{"likes"};
			$topsong=$tsongs{$key}{"songname"};
		}
	}
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
		<link rel="icon" href="http://widit.knu.ac.kr/~adit/proj/resources/images/$uinfo{$uname}{avatar}">

		<!--* Scripts to preview&save user's image depending on their selection *-->
		<script>
			<!-- "avatar" is the image id of main,big image on left; (a) holds which avatarButton was pressed -->
			function changePic(a) {
				document.getElementById("avatar").src=a;
			}
		</script>

	</head>

    <body style="padding:20px">
	<script src="http://widit.knu.ac.kr/~adit/proj/player/Drums_Piano.js"></script>
    <script src="http://widit.knu.ac.kr/~adit/proj/player/PlayFunctions.js"></script>
		<h2 style='text-align: center;'>My Profile</h2>

			<div class="row">
				<div style="display: inline-block">

					<!-- left hand side of the page -->
					<div class="left">
							<!--Create a card of the user's profile picture and name in "main section"-->
							<div class="polaroid" style="width: 400px; ">
								<img id="avatar" src="http://widit.knu.ac.kr/~adit/proj/resources/images/$uinfo{$uname}{'avatar'}">
								<div class="cardtext">
									<h3>$uname</h3>
								</div>
							</div>

							<!-- Top Liked section -->
							<div id="rcorners3">
								<h3 style='text-align: center;'> $uname's Top Tune: </h3>
								<br>
								<img src="http://widit.knu.ac.kr/~adit/proj/resources/images/no1.png" style='display:block; margin: auto;'>
								<br>
								<h4 style='text-align: center;'>Song: $topsong &nbsp Likes:$toplikecount</h4>
								<br>
							</div>
					</div>

                    <!-- the right hand side of the page-->
					<div style="display: inline-block">
						<div style="padding:50px">

							<!-- Profile pic selection: an unordered list of buttons with images inside -->
							<div id="rcorners">
								<h3>Preview Avatars</h3>
								<br>
								<div id="scroll">
								<ul>
									<div class="selector">
									<li><button onclick='changePic("http://widit.knu.ac.kr/~adit/proj/resources/images/avatar1.jpg");'><img src="http://widit.knu.ac.kr/~adit/proj/resources/images/avatar1.jpg"><span>Swag</span></button></li>
									<li><button onclick='changePic("http://widit.knu.ac.kr/~adit/proj/resources/images/avatar2.jpg");'><img src="http://widit.knu.ac.kr/~adit/proj/resources/images/avatar2.jpg"><span>Pink</span></button></li>
									<li><button onclick='changePic("http://widit.knu.ac.kr/~adit/proj/resources/images/avatar7.jpg");'><img src="http://widit.knu.ac.kr/~adit/proj/resources/images/avatar7.jpg"><span>Blue</span></button></li>
									<li><button onclick='changePic("http://widit.knu.ac.kr/~adit/proj/resources/images/avatar3.jpg");'><img src="http://widit.knu.ac.kr/~adit/proj/resources/images/avatar3.jpg"><span>Frog</span></button></li>
									<li><button onclick='changePic("http://widit.knu.ac.kr/~adit/proj/resources/images/avatar4.jpg");'><img src="http://widit.knu.ac.kr/~adit/proj/resources/images/avatar4.jpg"><span>Crown</span></button></li>
									<li><button onclick='changePic("http://widit.knu.ac.kr/~adit/proj/resources/images/avatar5.jpg");'><img src="http://widit.knu.ac.kr/~adit/proj/resources/images/avatar5.jpg"><span>Chain</span></button></li>
									<li><button onclick='changePic("http://widit.knu.ac.kr/~adit/proj/resources/images/avatar6.jpg");'><img src="http://widit.knu.ac.kr/~adit/proj/resources/images/avatar6.jpg"><span>Fairy</span></button></li>
									</div>
								</ul>
								</div>
								<br>

								<!-- form to save user's selection -->
								<form action="profile.cgi" method="post">
									<div style='padding:10px;'>
										<h3>Select your Avatar:</h3>

										<input type="radio" value="avatar1.jpg" id="avatar1" name="avatar">
										<label for="avatar1">Swag</label>
										<input type="radio" value="avatar2.jpg" id="avatar2" name="avatar">
										<label for="avatar2">Pink</label>
										<input type="radio" value="avatar7.jpg" id="avatar7" name="avatar">
										<label for="avatar7">Blue</label>
										<input type="radio" value="avatar3.jpg" id="avatar3" name="avatar">
										<label for="avatar3">Frog</label>
										<input type="radio" value="avatar4.jpg" id="avatar4" name="avatar">
										<label for="avatar4">Crown</label>
										<input type="radio" value="avatar5.jpg" id="avatar5" name="avatar">
										<label for="avatar5">Chain</label>
										<input type="radio" value="avatar6.jpg" id="avatar6" name="avatar">
										<label for="avatar6">Fairy</label>
									</div>
						    	<input class="sbutton" type="submit" value="Save" id="save">
						  	</form>

							</div>

							<br>
							<hr>
							<br>
                            <!-- Music Library Display -->
							<div id="rcorners2">
								<nav>
									<h3>Music</h3>
									<ol>	
EOP
foreach $song(@songs) {
	@songinfo=split(/\Q$songinner\E/,$song);
	print<<EOP;
    <tr>
	<form action="profile.cgi" method="post">
	<input type="hidden" id="songid" name="songid" value="$songinfo[0]">
    <li><text id="1">$songinfo[1]</text>&nbsp&nbsp<text id="1">( $songinfo[2] )</text><button type="submit" style="float:right;"> Delete </button>  <input style="float:right;" type="button" value="Play" onclick="playtext('$songinfo[2]')"></li>
	<hr>
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
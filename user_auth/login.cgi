#!/usr/bin/perl -w

use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);
use utf8;
use Encode;

# get input
$uname=param("uname");
$pw=param("pw");
chomp $uname;
chomp $pw;
$file="../resources/files/user_info.out";
# delimiter character to separate text fields in file
$delim="!---!";


# Checking if any parameters are empty, and store error message in array @emptyparams
@emptyparams=();
if($uname eq "")
{
    push(@emptyparams,"User ID");
}
if($pw eq "")
{
    push(@emptyparams,"Password");
}

$errmsg=join(" and ",@emptyparams);
if((scalar @emptyparams)>0)
{
    print header();
    $headerphp=system '/usr/bin/php', '../landing_page/nav_land.php';
    print<<EOP;
   <html>
   <head>
    <meta charset="utf-8">
    <title>Virtual Piano</title>
    <link rel="stylesheet" href="style_error.css">
    <title>Empty Input</title>
    </head>
    <body>
    <h1 class="oops">Bad Input</h1>
    <h2 class="type">No field must be <font color='red'>empty</font></h2>
    <h3 class="obs">The following fields are empty<font color="purple">$errmsg</font></h3>
    <br><br>
    Please <a href="login.html">go back and try again</a></p>
    </body>
    </html>
EOP
exit;
}
#------------------------------------------------------------------------

# Getting user_info.out into hash------------------------------------
open(IN,"<$file") || die "can't read $file";
@lines=<IN>;
close(IN);
@temp=();
%uinfo=();
foreach $line(@lines)
{
    chomp $line;
    @temp=split(/\Q$delim\E/,$line);
    $uinfo{$temp[0]}=$temp[1];
}
#----------------------------------------------------------------------

#if userid doesn't exists
if(!exists($uinfo{$uname})) {
    print header();
    $headerphp=system '/usr/bin/php', '../landing_page/nav_land.php';
    print<<EOP;
   <html>
   <head>
    <meta charset="utf-8">
    <title>Virtual Piano</title>
    <link rel="stylesheet" href="style_error.css">
    <title>Empty Input</title>
    </head>
    <body>
    <h1 class="oops">Invalid Username</h1>
    <h2 class="type"><font color='purple'>$uname</font> doesn't exist</h2>
    <h3 class="obs">Please try again with a different username or Create a new account</h3>
    <br><br>
    <p style="font-size:20px"><a href="login.html">Login Again</a>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<a href="signup.html">Sign Up</a></p>
    </body>
    </html>
EOP
exit;
}

#if password is correct
if(($uinfo{$uname}) eq $pw) {
    $cookie= cookie(
    -name => "VP-cookie",
    -value => "$uname",
    -path => "/~adit/",);

   
    print header(-cookie=>$cookie,-charset=>'utf-8');
    $headerphp=system '/usr/bin/php', '../header_footer/nav.php';
    print<<EOP;
   <html>
   <head>
    <meta charset="utf-8">
    <title>Virtual Piano</title>
    <link rel="stylesheet" href="style_error.css">
    <title>Login Success</title>
    </head>
    <body>
    <h1 class="oops"><font color="green">Login Success</font></h1>
    <h2 class="type">Welcome <b><i>$uname</b></i></h2>
    <h3 class="obs"><a href="http://widit.knu.ac.kr/~adit/proj/player/piano.cgi">Please click here to go to piano player</a></h3>
    <br><br>
    </body>
    </html>
EOP
exit;
}
if(($uinfo{$uname}) ne $pw) 
{
    print header();
    $headerphp=system '/usr/bin/php', '../landing_page/nav_land.php';
    print<<EOP;
   <html>
   <head>
    <meta charset="utf-8">
    <title>Invalid Password</title>
    <link rel="stylesheet" href="style_error.css">
    <title>Invalid Password</title>
    </head>
    <body>
    <h1 class="oops">Invalid Password</h1>
    <h2 class="type">Password doesn't match</h2>
    <h3 class="obs"><a href="./login.html">Please try again</a></h3>
    <br><br>
    </body>
    </html>
EOP
exit;
}
else
{
    print header();
    $headerphp=system '/usr/bin/php', '../landing_page/nav_land.php';
    print<<EOP;
   <html>
   <head>
    <meta charset="utf-8">
    <title>Unknown Error</title>
    <link rel="stylesheet" href="style_error.css">
    <title>Unknown Error</title>
    </head>
    <body>
    <h1 class="oops">Unknown Error</h1>
    <h2 class="type">Please go back and try again/h2>
    <h3 class="obs"><a href="./login.html">Login page</a></h3>
    <br><br>
    </body>
    </html>
EOP
exit;
}

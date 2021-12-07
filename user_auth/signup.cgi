#!/usr/bin/perl -w

use CGI qw(:standard -debug);
use CGI::Carp qw(fatalsToBrowser);
use utf8;
use Encode;

# get input
$uname=param("uname");
$pw=param("pw");
$pw2=param("pw2");
$file="../resources/files/user_info.out";
# Delimiter character for text field storage
$delim="!---!";


# Checking if any parameters are empty, and storing error message in array @emptyparams
@emptyparams=();
if($uname eq "")
{
    push(@emptyparams,"User ID");
}
if($pw eq "")
{
    push(@emptyparams,"Password");
}
if($pw2 eq "")
{
    push(@emptyparams,"Password Confirmation");
}

$checklist=join(", ",@emptyparams);
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
    <h3 class="obs">The following fields are empty<font color="purple">$checklist</font></h3>
    <br><br>
    Please <a href="signup.html">go back and try again</a></p>
    </body>
    </html>
EOP
exit;
}

# Checking if any fields contain the delimiter character sequence
# the delimiter is used to seperate fields in the hw9-1.out file. If the field themselves contain it, it would cause problems when reading.
@paramconflicts=();
if($userid =~ /\Q$delim\E/)
{
    push(@paramconflicts,"User ID");
}
if($pw=~ /\Q$delim\E/)
{
    push(@paramconflicts,"Password");
}
if($pw2=~ /\Q$delim\E/)
{
    push(@paramconflicts,"Password Confirmation");
}

$checklist=join("<br>",@paramconflicts);
if((scalar @paramconflicts)>0)
{
    print header();
    $headerphp=system '/usr/bin/php', '../landing_page/nav_land.php';
    print<<EOP;
   <html>
   <head>
    <meta charset="utf-8">
    <title>Virtual Piano</title>
    <link rel="stylesheet" href="style_error.css">
    <title>Bad Input</title>
    </head>
    <body>
    <h1 class="oops">Bad Input</h1>
    <h2 class="type">No field must contain <font color='red'>$delim</font> characters</h2>
    <h3 class="obs">The following fields contain the illegal character sequence, <font color="purple">$checklist</font></h3>
    <br><br>
    The character sequence, $delim, is reserved for internal server operations.<br><br>
    Please <a href="signup.html">go back and try again</a></p>
    </body>
    </html>
EOP
exit;
}

# Checking if id already exists
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
if(exists($uinfo{$uname})){
    print header();
    $headerphp=system '/usr/bin/php', '../landing_page/nav_land.php';
    print<<EOP;
   <html>
   <head>
    <meta charset="utf-8">
    <title>Virtual Piano</title>
    <link rel="stylesheet" href="style_error.css">
    <title>Invalid Input</title>
    </head>
    <body>
    <h1 class="oops">Username Unavailable</h1>
    <h2 class="type"><font color='purple'>$uname</font> already exists</h2>
    <h3 class="obs">Please try again with a different username or Login with your old username</h3>
    <br><br>
    <a href="signup.html">Signup Again</a>&nbsp&nbsp<a href="login.html">Login</a></p>
    </body>
    </html>
EOP
exit;
}
if($pw ne $pw2)
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
    <h1 class="oops">Password Mismatch</h1>
    <h2 class="type">Passwords don't match</h2>
    <h3 class="obs"><a href="./signup.html">Please try again</a></h3>
    <br><br>
    </body>
    </html>
EOP
exit;
}
else {
    open(OUTF,">>","$file") || die "can't append to $file";
    print OUTF $uname.$delim.$pw."\n";
    close(OUTF);
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
    <h1 class="oops"><font color="green">SignUp Success</font></h1>
    <h2 class="type">Welcome <b><i>$uname</b></i></h2>
    <h3 class="obs"><a href="http://widit.knu.ac.kr/~adit/proj/player/piano.cgi">Please click here to go to piano player</a></h3>
    <br><br>
    </body>
    </html>
EOP
exit;
}
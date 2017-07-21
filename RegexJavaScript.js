/*  Regular Expressions in JavaScript
    Herman Leung
    21 July 2017

    Table of Contents
    1. Basics
    2. Functions
    3. Flags
    4. Character classes
    5. Ranges
    6. Groups
    7. Quantifiers
    8. Anchors
    9. Assertions
    10. References and tools  */

// ====================================================================
// === 1. Basics - Characters, strings, and escaping with backslash ===
// ====================================================================

// Backslash for quotes and apostrophes in string notation

var text = "She said, \"I'm going to eat six spoons of fresh snow peas.\" ";
var text2 = 'She said, "I\'m going to eat six spoons of fresh snow peas." ';

text === text2; // true

//   In regex patterns, functional chars may need to be escaped
//   if you want the literal character; they include (more on these later)
//        . + ? * - [ ] ( ) \ / ^ $ |

// 'I (Caesar) came, I saw, I conquered'.search(/(/); // cannot be parsed
'I (Caesar) came, I saw, I conquered'.search(/\(/);

// But, okay without backslash in contexts where it cannot have a functional interpretation
'I (Caesar) came, I saw, I conquered'.search(/[(]/);

// The backslash does not affect all chars
'='.search(/=/);
'='.search(/\=/);

// Some chars are always escaped
console.log('a\na'); // \n - new line / line feed (LF)
console.log('a\rb'); // \r - carriage return (CR)
console.log('a\ta'); // \t - tab
// Uncommon: \b - backspace, \v - vertical tab, \f - page break/form feed

// Hexadecimal and unicode chars
'\xe3';   // \x + 2 chars /[0-9a-f]/i
'\u8003'; // \u + 4 chars /[0-9a-f]/i

// Astrals
'\u{1F4A9}'; // ES6 \u + up to 6 chars inside curly brackets
'\uD83D\uDCA9'; // ES5 equivalent
// NOTE 1: Astrals are implemented as composed of 2 chars
// NOTE 2: There are other composed chars that look like 1 char but are many

// BACKSLASH FOR MULTI-LINE STRING

// In ES6, the backticks `` allow you to spread a string across multiple lines,
// and all the white space is included in the string

`Three blind mice
    see how they run!`;

// If you use single or double quotes, you can use the backslash to spread a
// string across multiple lines, and line breaks are ignored (but not char space).

'Three blind mice \
    see how they run!';

var str = 'Three blind mice \
           see how they run!';
str;


// ====================
// === 2. Functions ===
// ====================
/*
    FUNCTION    USAGE                           RETURNS
                                                (NO MATCH)  (MATCH)

    .match()    <str>.match(<regex>)            null        [first match, index of match, input string]
                                with flag 'g'   null        array of all the matches only (no indexes or input string)
    .exec()     <regex>.exec(<string>)          null        [match, index of match, input string]

    .search()   <str>.search(<regex>)           -1          index of the first match

    .replace()  <str>.replace(<regex>, <str>)   new string with replacements

    .test()     <regex>.test(<string>)          false       true
*/

// .match() --> returns array of first match (returns all matches with flag g)
//              returns null if no match
'abcda'.match(/a/);
'abcda'.match(/a/g);
'abcda'.match(/z/);

// .exec() --> returns array of first match (or one match at a time with flag g);
//         --> returns null if no match
const RE = /a/;
RE.exec('abcda');
RE.exec('wxyzw');

RE = /a/g;
RE.exec('abcda');
RE.exec('abcda');

// .search() --> returns index of first match; returns -1 if no match
'abcda'.search(/a/);
'abcda'.search(/z/);

// .replace()
'abcda'.replace(/a/, 'Z');

// .test() --> returns true or false
/a/.test('abcda');
/z/.test('abcda');


// ================
// === 3. Flags ===
// ================
/*
    g (global)          used with .match() and .exec(), finds all (not just the first)
    i (ignore case)     does not distinguish lower and upper case
    m (multiline)       tells ^ and $ to treat \n or \r as boundaries (more later)
    u (unicode)         treats the regex pattern as unicode (may need it when encountering encoding errors)
*/

'ABCDA'.match(/A/g);
'ABCDA'.search(/b/i);
'Dogs are funny.\nDogs are hairy.'.match(/^D/gm);
'Dogs are funny.\nDogs are hairy.'.match(/\.$/gm);


// ============================
// === 4. Character classes ===
// ============================
/*
    \d = numerical    \D = non-numerical
    \w = word         \W = non-word           ('word' here means alphanumeric and underscore)
    \s = white space  \S = not white space
*/

'123'.search(/\d/);
'123'.search(/\D/);

'abc'.match(/\w/g);
'abc'.match(/\W/g);

'\t\r\n'.replace(/\s/g, 'Y');
'\t\r\n'.match(/\S/g, 'Y');


// =================
// === 5. Ranges ===
// =================
/*  NOTE: All of the below match patterns of 1 character only

    [] - range specification
    [^ ] - range specification - excluding
    . - everything except \n
    | - or
*/

'I ain\'t got no money, yo!'.match(/[',!]/g);
'I ain\'t got no money, yo!'.match(/[^',!]/g);
'I ain\'t got no money, yo!'.replace(/[a-z]/gi, '_');

'.'.search(/./);
'\n'.search(/./);

// So if you really want to include everything, use .|\n
'Line\nLine'.match(/.|\n/g);

// | -- or
/da|bf/.test('daf');
/da|bf/.test('dbf');
/da|bf/.test('dzf');


// ===========================
// === 6. Groups - with () ===
// ===========================
/*
    ( )     Capturing group
    (?: )   Non-capturing group
    \1      group referencing within regex pattern

    // Used with .replace() in the replacement string
    $1      insert captured group ($2 = 2nd captured group, $3 = 3rd, etc.)
    $`      insert string preceding (1st) captured group
    $'      insert string following (1st) captured group
    $&      insert entire match
*/

// What if you want to use the | over more than one char?
// Use () to contain the multi-char alternatives
'aabbaaaaccaa'.match(/aa(BB|CC)aa/g);

// The parentheses also has a "grouping" function (let's use .match() without the g flag)
'aaBBaaaaCCaa'.match(/aa(BB|CC)aa/); // [ 'aaBBaa', 'BB', index: 0, input: 'aaBBaaaaCCaa' ]
                                     // Notice the 'BB' captured by the ()

// Because .match() only returns the matches if there are more than one match,
// here's where .exec() would be useful for getting the stuff inside the parentheses

'aaBBaaaaCCaa'.match(/aa(BB|CC)aa/g); // .match() with g flag won't return the group captures

// But .exec() allows us get the group captures of all matches, using a loop
REGEX = /aa(BB|CC)aa/g;
str = 'aaBBaaaaCCaaaaBBaa';
var myArray;
while ((myArray = REGEX.exec(str)) !== null) {
    console.log(myArray);
}

// Grouping also allows reference back to the captured group
'dada'.match(/(da)\1/); // [ 'dada', 'da', index: 0, input: 'dada' ]
'data'.match(/(da)\1/); // null

// NOTE: the reference is to what is captured, not the pattern itself!
'datata'.match(/(da|ta)\1/); // ['tata']
'datata'.match(/([dt]a)\1/); // ['tata']

// You can have as many groups as you want
'tadatada'.match(/(ta)(da)\1\2/);
'abcdefghijklabcdefghijkl'.match(/(a)(b)(c)(d)(e)(f)(g)(h)(i)(j)(k)(l)\1\2\3\4\5\6\7\8\9\10\11\12/);

// The numbering depends on the order in which the ( appears
// For example, in the case of nested groups
'tatatat'.match(/((t|d)a)\1\2/);

// If you don't want the parentheses to make a capture, use (?: )
'aaBBaa'.match(/aa(?:BB|CC)aa/);

// If you want to reference a captured group in the replacement string in .replace()
'HyperText Markup Language'.replace(/([a-z])([A-Z])/, '$1 $2');

// To get string before match pattern, use $` (dollar sign + backtick)
'hyperTEXT MARKUP'.replace(/[A-Z]/, '$`');
'hyperTEXT MARKUP'.replace(/[A-Z]/, '<$`>'); // better visualization

// To get string after matched pattern, use $' (or $\' if using single quotes)
'hyperTEXT MARKUP'.replace(/[A-Z]/, "$'");
'hyperTEXT MARKUP'.replace(/[A-Z]/, "<$'>");
'hyperTEXT MARKUP'.replace(/[A-Z]/, '<$\'>'); // better visualization

// To get the entire matched pattern, use $&
'hyperTEXT MARKUP'.replace(/[A-Z]/, '$&$&$&');
'hyperTEXT MARKUP'.replace(/[A-Z]/, '<$&$&$&>'); // better visualization


// ======================
// === 7. Quantifiers ===
// ======================
/*
    ?       appears 0 or 1 time | ALSO non-greedy when appearing after * or +
    *       appears 0 or any number of times
    +       appears 1 or more times

    {2}     appears 2 times
    {3,5}   appears 3-5 times
    (4,)    appears at least 4 times
*/

// ? --> appears 0 or 1 time
// Optional parentheses for country code in phone numbers
'852 2345 6789'.search(/^\(?852\)?/);
'(852) 2345 6789'.search(/^\(?852\)?/);

// * --> appears 0 or any amount of times
// Get all words with "watch" followed by any number of letters
'watch, watchy, watched, watching'.match(/watch[a-z]*/g);

// + --> appears 1 or more times
// Get all continuous alphabetical strings
"My name is R2D2. I'm a robot.".match(/[A-Za-z]+/g);

// NOTE: * and + are by default "greedy".
// That means it will search until the very last instance of the char pattern after * or +,
//    and return everything in between
"My name is R2D2. I'm a robot.".match(/^.+\./g); // bad attempt at getting only one sentence
"My name is R2D2. I'm a robot.".match(/^.+?\./g); // non-greedy ? to the rescue

var htmlStr = '<div class="container">Container</div><div class="jumbotron">Header</div>';
htmlStr.match(/<div class="container">.+<\/div>/); // bad attempt at getting the container div
htmlStr.match(/<div class="container">.+?<\/div>/); // non-greedy ? to the rescue

// NOTE: The above doesn't take care of nested divs,
//       and nested things are complicated to do in regex
//          --> Use an html parser module instead!

// {} --> exact (and greedy) quantification
'The flower bloomed in the wild wind.'.match(/\w{4}/g); // 4-letter strings
'The flower bloomed in the wild wind.'.match(/\w{4,6}/g); // 4-6 letters
'The flower bloomed in the wild wind.'.match(/\w{4,}/g); // 4 or more letters


// ==================
// === 8. Anchors ===
// ==================

// NOTE: These DON'T represent actual characters

/*
*/

"There's a rainbow here.\nThere's a rainbow there.".match(/^There's/g);
"There's a rainbow here.\nThere's a rainbow there.".match(/^There's/gm); // m flag

"There's a rainbow here.\nThere's a rainbow there.".match(/t?here\.$/g);
"There's a rainbow here.\nThere's a rainbow there.".match(/t?here\.$/gm); // m flag

"My name is R2D2. I'm a robot.".match(/\b.+?\b/g);
"My name is R2D2. I'm a robot.".match(/\b\w+?\b/g); // just the words


// =====================
// === 9. Assertions ===
// =====================
/*
    (?= )   positive lookahead
    (?! )   negative lookahead
*/

// (?= ) -- > positive lookahead
'aaBBaaCCaa'.match(/aa(BB|CC)(?=aa)/g);

// Although assertions make use of parentheses, they DON'T trigger grouping
'aaBBaa'.match(/aaBB(?=aa)/);

// (?! ) --> Negative lookahead
'aaBBaaaaBB--'.match(/aaBB(?!aa)/);

// Why use assertions?
// 1. You don't want to capture the string inside the assertion
// 2. You want to get overlapping matches (normally you can't)

'aaBBaaBBaa'.match(/aaBBaa/g);
/*  What happens step by step:

    1. 'aaBBaaBBaa' --> MATCH 'aaBBaa', REMAINING SEARCH POOL '______BBaa'
    2. '______BBaa' --> NO MATCH
    3. END SEARCH, RETURN ['aaBBaa']
*/

'aaBBaaBBaa'.match(/aaBB(?=aa)/g);
/*  What happens step by step:
    1. 'aaBBaaBBaa' --> MATCH 'aaBB', REMAINING SEARCH POOL '____aaBBaa'
    2. '____aaBBaa' --> MATCH 'aaBB', REMAINING SEARCH POOL '________aa'
    3. '________aa' --> NO MATCH
    4. END SEARCH, RETURN ['aabb', 'aabb']
*/

/*
Unfortunately, JS doesn't have lookbehind - because they forgot about it!
As of ES8, it's still not available.
There are some workarounds, but they can get very complicated.
*/


// ================================
// === 10. References and tools ===
// ================================

/*
MDN documentation: https://developer.mozilla.org/en/docs/Web/JavaScript/Guide/Regular_Expressions
Javascript regex cheatsheet: https://www.debuggex.com/cheatsheet/regex/javascript
Regex tool 1: http://regexr.com/
Regex tool 2: https://regex101.com/
Atom regex helper: regex-railroad-diagram (installable package)

NOTE: Different programming languages have different implementations
of regular expressions / pattern matching functions, although the basics are
usually the same.

PostgreSQL: https://www.postgresql.org/docs/9.6/static/functions-matching.html
Python: https://docs.python.org/3/library/re.html
*/

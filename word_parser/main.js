var esrever = require('esrever');

var casper = require('casper').create({
  //verbose : true,
  //logLevel: "debug"
});

casper.options.clientScripts.push('./jquery-3.1.1.js');
casper.options.clientScripts.push('./data.js');
casper.options.waitTimeout = 1000000;

casper.on('remote.message', function (msg) {
  this.echo('remote message caught: ' + msg);
});

function getSeasons() {
  var resultArr = [];

  var seasonEls = $("#left_sidebar > .ill-levels.active > .ill-seasons-list > a");

  console.log(seasonEls.length + " season elements found");

  $(seasonEls).each(function (index, seasonEl) {
    //// TODO remove this block and uncomment the one below
    //if (index < 1) {
    //  var resultRow = {};
    //
    //  resultRow.href  = $(seasonEl).attr('href');
    //  resultRow.title = $(seasonEl).text();
    //
    //  resultArr.push(resultRow);
    //}

    var resultRow = {};

    resultRow.href  = $(seasonEl).attr('href');
    resultRow.title = $(seasonEl).text();

    resultArr.push(resultRow);
  });

  return resultArr;
}

function getLessons() {
  var resultArr = [];

  var lessonsList = $(".main_content > .ill-lessons-list > .audio-lesson");

  console.log(lessonsList.length + " lesson elements found");

  $(lessonsList).each(function (index, lesson) {
    // TODO remove and uncomment the block below
    if (index < 57) {
      var resultRow = {};

      resultRow.href        = $(lesson).find(".wrapper-title-description > a").attr('href');
      resultRow.lessonNum   = $(lesson).find(".number").text();
      resultRow.lessonTitle = $(lesson).find(".wrapper-title-description > a").text();

      resultArr.push(resultRow);
    }

    //var resultRow = {};
    //
    //resultRow.href = $(lesson).find(".wrapper-title-description > a").attr('href');
    //resultRow.lessonNum = $(lesson).find(".number").text();
    //resultRow.lessonTitle = $(lesson).find(".wrapper-title-description > a").text();
    //
    //resultArr.push(resultRow);
  });

  return resultArr;
}

function getAudioTracks() {
  var resultArr = [];

  var audioDivs = $(".lesson-playlist .playlist .lesson-media");

  $(audioDivs).each(function (index, audioDiv) {
    var resultRow = {};

    resultRow.url  = $(audioDiv).find(".media-play").attr('data-url');
    resultRow.name = $(audioDiv).find(".media-play").text();

    resultArr.push(resultRow);
  });

  return resultArr;
}

function getLessonText() {
  var resultArr = [];

  var allBlock = $("#lesson_lbl_transcripts__container .lesson-lbl-transcript.all");

  var langHeaders = $(allBlock).find(".lbl-langheader");
  var langTables  = $(allBlock).find(".lesson-lbl-table");
  console.log("found " + langHeaders.length + " lang headers");
  for (var i = 0; i < langHeaders.length; i++) {
    var resultRow = {};

    var langHeader = langHeaders[i];
    var langTable  = langTables[i];

    resultRow.langVersion = $(langHeader).text();
    console.log(resultRow.langVersion);

    var textLines = $(langTable).find("tbody > tr");

    resultRow.textLines = [];
    $(textLines).each(function (index, textLine) {
      var textAudio = $(textLine).find("td.cplaybutton > .relative-container > .ill-onebuttonplayer > .mejs-container > .mejs-inner > .mejs-mediaelement > .me-cannotplay > a").attr('href');
      var text      = $(textLine).find("td.ctext .clickable").text();

      resultRow.textLines.push({
        audioLink: textAudio,
        text     : text
      });
    });

    resultArr.push(resultRow);
  }

  return resultArr;
}

var level = casper.cli.get(0);

if (level) {
  var fs = require('fs');

  var seasons         = [];
  var lessonsBySeason = [];

  casper.start('https://www.chineseclass101.com/index.php', function () {
    this.waitForSelector("input[name='amember_login']");
  });

  casper.then(function () {
    this.echo('currentUrl: ' + this.getCurrentUrl());

    this.fill("form[name='signin']", {
      'amember_login': 'BigJK688454233',
      'amember_pass' : 'Meredith!1'
    }, true);
  });

  casper.then(function () {
    this.echo('currentUrl: ' + this.getCurrentUrl());
    var url = "https://www.chineseclass101.com/index.php?cat=" + level;
    casper.then(function () {
      casper.open(url).then(function () {
        this.waitForSelector("#left_sidebar .ill-levels.active", function () {
          this.echo(this.getCurrentUrl());

          seasons = this.evaluate(getSeasons);
        });
      });
    });
  });

  casper.then(function () {
    casper.each(seasons, function (self, season) {
      this.thenOpen(season.href, function () {
        this.echo(this.getCurrentUrl());
        this.waitForSelector("div.ill-lessons-list", function () {
          var lessons = this.evaluate(getLessons);
          this.echo(lessons.length);

          lessonsBySeason.push({
            season : season,
            lessons: lessons
          });
        });
      });
    });
  });

  casper.then(function () {
    casper.each(lessonsBySeason, function (self, lessonBySeason) {
      casper.each(lessonBySeason.lessons, function (self, lesson) {
        this.thenOpen(lesson.href, function () {
          this.echo(this.getCurrentUrl());
          this.thenClick("[data-route='lesson-materials'] > span > span", function () {
            this.waitForSelector("#lesson_lbl_transcripts__container", function () {
              var audioTracks    = this.evaluate(getAudioTracks);
              lesson.audioTracks = audioTracks;

              var lessonText   = this.evaluate(getLessonText);
              lesson.sentences = lessonText;
            });
          });
        });
      });
    });
  });

  casper.then(function () {
    var fs   = require('fs');
    var save = fs.pathJoin(fs.workingDirectory, 'Chinese Class 101', level);
    fs.write(save, JSON.stringify(lessonsBySeason), 'a');
  });
} else {
  this.echo("You must include a book number, book prefix and chapter to continue");
}

casper.run();
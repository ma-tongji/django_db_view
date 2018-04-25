//slide_show.js ver 1.0

/* load js and css manually if the page have't load them

(function(e, s) {
    e.src = s;
    e.onload = function() {
        jq = jQuery.noConflict();
        console.log('jQuery injected');
    };
    document.head.appendChild(e);
})(document.createElement('script'), '//code.jquery.com/jquery-latest.min.js')

jq('body').append(jq('<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/smoothness/jquery-ui.css">'))
jq('body').append(jq('<link rel="stylesheet" href="http://localhost/img_board/static/css/slideshow.css">'))
jq('body').append(jq('<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">'))
jq('body').append(jq('<script src="//code.jquery.com/ui/1.12.1/jquery-ui.js"></script>'))
*/


var SlideShow = {
  init: function(keylist, image_url='') {
    jq = $; //jQuery.noConflict();
    var self = {};
    self.images = [];
    self.index = 0;
    self.interval_id = -1; // -1 not set

    for(var i=0; i<keylist.length; i++) {
      jq(keylist[i].selector).each(function() {
        if (jq(this)) {
          img_src = jq(this).attr(keylist[i].attrib)
          self.images.push(img_src);
          jq(this).click({'img_src': img_src}, function(event) {
            self.slide_locate(event.data.img_src);
            self.slide_show();
            //console.log(img_src)
            return false;
          })
          //console.log(self.images);
        }
      });
    }

    var full_cover_div = `
    <div class="full-cover" style="display:none;">
      <img src="`+self.images[self.index]+`" />
      <img class="preload" />
      <div class="slide-control slide-left">❮</div>
      <div class="slide-control slide-right">❯</div>
      <div class="slide-control-panel">
        <div class="slide-control slide-close">✖</div>
        <div class="slide-control slide-auto"><span class="glyphicon glyphicon-play"></span></div>
        <div class="slide-control slide-stop"><span class="glyphicon glyphicon-pause"></span></div>
      </div>
    </div>`;
    jq('body').append(full_cover_div);


    self.slide_shift = function(shift_i) {
      self.index = (self.index + shift_i + self.images.length) % self.images.length;
      jq('.full-cover img').attr('src', self.images[self.index]);
      jq('.preload').attr('src', self.images[(self.index+1) % self.images.length]);
    };

    self.slide_locate = function(url) {
      self.index = self.images.indexOf(url);
      if (self.index == -1) {
        self.index = 0;
      }
      jq('.full-cover img').attr('src', self.images[self.index]);
      jq('.preload').attr('src', self.images[(self.index+1) % self.images.length]);
    };

    self.slide_show = function() {
      // create full-div
      jq('.full-cover').show();
    }

    self.slide_close = function() {
      jq('.full-cover').remove();
    }


    jq('.slide-right').click(function() {
      self.slide_shift(1);
    });
    jq('.slide-left').click(function() {
      self.slide_shift(-1);
    });
    jq('.slide-close').click(function() {
      jq('.full-cover').hide();
    });
    jq('.slide-auto').click(function() {
      self.interval_id = window.setInterval(function(){self.slide_shift(1)}, 2000);
    });
    jq('.slide-stop').click(function() {
      window.clearInterval(self.interval_id);
      self.interval_id = -1;
    });

    return self;
  }
};

//  ss = SlideShow.init(
//    [{'selector':'img', 'attrib':'src'}], 
//    image_url='http://www.ruanyifeng.com/blog/images/sup_geekbang_20180212b.jpg'
//  )
//
//  jq('body').append(jq('<link rel="stylesheet" href="http://localhost/img_board/static/css/slideshow.css">'))
//  jq('body').append(jq('<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">'))
//  jq('img').click(function(){
//    ss.slide_locate(this.href);
//    ss.slide_show();
//    return false;
//  })
//
//};


/* deprecated

if (typeof jQuery == 'undefined') {
  var s = document.createElement('script');
  s.src = '//code.jquery.com/jquery-1.12.4.js';
  s.onload = function() {
    console.log('jQuery injected from slideshow');
  };
  document.head.append(s);
} else {
  jq=jQuery;
}
*/

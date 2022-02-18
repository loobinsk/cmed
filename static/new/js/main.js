(function($) {
  "use strict";

  // Mask
  function mask() {
    $(".phone-mask").mask("+7 (000) 000-00-00", {
      placeholder: "+7 (___) ___-__-__",
    });
  }

  // slider Main-slider
  function sliderMain() {
    var prev = $("#prevMain");
    var next = $("#nextMain");
    $(" .main-slider  .slick-slider").slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      arrows: false,
      autoplay: true,
      autoplaySpeed: 4000,
      dots: true,
      infinite: true,
      prevArrow: prev,
      nextArrow: next,
    });
  }
  // slider lecture
  function sliderLecture() {
    $(" .lecture  .slick-slider").slick({
      slidesToShow: 2,
      slidesToScroll: 1,
      arrows: false,
      autoplay: true,
      autoplaySpeed: 4000,
      dots: true,
      infinite: true,
      variableWidth: true,
      responsive: [
        {
          breakpoint: 992,
          settings: {
            variableWidth: false,
            slidesToShow: 1,
            slidesToScroll: 1,
          },
        },
      ],
    });
  }

  // slider video
  function sliderVideo() {
    $(" .video  .slick-slider").slick({
      slidesToShow: 2,
      slidesToScroll: 1,
      arrows: false,
      autoplay: true,
      autoplaySpeed: 4000,
      dots: true,
      infinite: true,
      variableWidth: true,
      responsive: [
        {
          breakpoint: 992,
          settings: {
            variableWidth: false,
            slidesToShow: 1,
            slidesToScroll: 1,
          },
        },
      ],
    });
  }

  // slider recommend
  function sliderRecommend() {
    $(" .recommend .slick-slider").slick({
      slidesToShow: 2,
      slidesToScroll: 1,
      arrows: false,
      autoplay: true,
      autoplaySpeed: 4000,
      dots: true,
      infinite: true,
      variableWidth: true,
      responsive: [
        {
          breakpoint: 992,
          settings: {
            variableWidth: false,
            slidesToShow: 1,
            slidesToScroll: 1,
          },
        },
      ],
    });
  }

  // Select2
  function select2() {
    $(".select2").select2({
      minimumResultsForSearch: -1,
      width: "100%",
      language: "ru",
    });
    $(".select2-placeholder").select2({
      minimumResultsForSearch: -1,
      placeholder: "Выберите опцию",
      width: "100%",
      language: "ru",
    });

    $(".js-select2").select2({
      placeholder: "Выберите",
      maximumSelectionLength: 2,
      language: "ru",
    });
  }

  // Fanycbox gallery
  function fancybox() {
    $('[data-fancybox*="slider-"]').fancybox({
      backFocus: false,
    });
  }

  function openMenuDrop(e) {
    e.preventDefault();
    var more = e.target
      .closest(".header__drop")
      .querySelector(".header__dropdown");
    var icon = e.target
      .closest(".header__drop")
      .querySelector(".header__drop-link-main");
    $(".header__drop .header__dropdown")
      .not(more)
      .removeClass("active");
    $(".header__drop .header__drop-link-main")
      .not(icon)
      .removeClass("rotate-after");
    more.classList.toggle("active");
    icon.classList.toggle("rotate-after");
  }

  function openMenu() {
    $(".header__navbar").toggleClass("active");

    $(document).mouseup(function(e) {
      if ($(".header__navbar").has(e.target).length === 0) {
        $(".header__navbar").removeClass("active");
      }
    });
  }

  function closeWebinarAlarm() {
    $(".webinar__alarm").hide();
  }

  function tabsOpen() {
    var jsTriggers = document.querySelectorAll(".js-tab-trigger");

    jsTriggers.forEach(function(item, i) {
      item.addEventListener("click", function() {
        var tabName = this.dataset.tab,
          tabContent = document.querySelector(
            '.js-tab-content[data-tab="' + tabName + '"]'
          );

        document
          .querySelectorAll(".js-tab-content.active")
          .forEach(function(item, i) {
            item.classList.remove("active");
          });

        document
          .querySelectorAll(".js-tab-trigger.active")
          .forEach(function(item, i) {
            item.classList.remove("active");
          });

        tabContent.classList.add("active");
        this.classList.add("active");
      });
    });
  }

  function openChat(e) {
    e.preventDefault();
    $(".personal-area__more-dialog").addClass("active");
  }
  function closeChat() {
    $(".personal-area__more-dialog").removeClass("active");
  }

  function openSurch() {
    if ($(window).width() < 1200) {
      $(".search").toggleClass("active");
    }
  }

  function textereaHeight() {
    document.querySelector("textarea").addEventListener("input", function(e) {
      e.target.style.height = "auto";
      e.target.style.height = e.target.scrollHeight + 2 + "px";
    });
  }

  $(document).ready(function() {
    mask();

    sliderMain();
    sliderLecture();
    sliderVideo();
    sliderRecommend();

    fancybox();
    select2();
    tabsOpen();

    $(".header__drop-link-main").click(openMenuDrop);
    $(".header__navbar-btn").click(openMenu);
    $(".webinar__alarm-btn").click(closeWebinarAlarm);
    $(".personal-area__white").click(openChat);
    $(".personal-area__chat-close").click(closeChat);
    $(".search__btn").click(openSurch);
    textereaHeight();


  });
})(jQuery);

// $(document).ready(function() {
//   $(this).click(function() {
//     $(this)
//       .$(".popup-fade")
//       .fadeIn();
//     $(".home").toggleClass("home-block");
//     console.log("ff");
//     return false;
//   });

//   $(".popup-close").click(function() {
//     $(this)
//       .parents(".popup-fade")
//       .fadeOut();
//     return false;
//   });

//   $(document).keydown(function(e) {
//     if (e.keyCode === 27) {
//       e.stopPropagation();
//       $(".popup-fade").fadeOut();
//     }
//   });

//   $(".popup-fade").click(function(e) {
//     if ($(e.target).closest(".popup").length == 0) {
//       $(this).fadeOut();
//     }
//   });
// });

!(function(e) {
  "function" != typeof e.matches &&
    (e.matches =
      e.msMatchesSelector ||
      e.mozMatchesSelector ||
      e.webkitMatchesSelector ||
      function(e) {
        for (
          var t = this,
            o = (t.document || t.ownerDocument).querySelectorAll(e),
            n = 0;
          o[n] && o[n] !== t;

        )
          ++n;
        return Boolean(o[n]);
      }),
    "function" != typeof e.closest &&
      (e.closest = function(e) {
        for (var t = this; t && 1 === t.nodeType; ) {
          if (t.matches(e)) return t;
          t = t.parentNode;
        }
        return null;
      });
})(window.Element.prototype);

document.addEventListener("DOMContentLoaded", function() {
  /* Записываем в переменные массив элементов-кнопок и подложку.
      Подложке зададим id, чтобы не влиять на другие элементы с классом overlay*/
  var modalButtons = document.querySelectorAll(".js-open-modal"),
    overlay = document.querySelector(".js-overlay-modal"),
    closeButtons = document.querySelectorAll(".js-modal-close");

  /* Перебираем массив кнопок */
  modalButtons.forEach(function(item) {
    /* Назначаем каждой кнопке обработчик клика */
    item.addEventListener("click", function(e) {
      /* Предотвращаем стандартное действие элемента. Так как кнопку разные
            люди могут сделать по-разному. Кто-то сделает ссылку, кто-то кнопку.
            Нужно подстраховаться. */
      e.preventDefault();

      /* При каждом клике на кнопку мы будем забирать содержимое атрибута data-modal
            и будем искать модальное окно с таким же атрибутом. */
      var modalId = this.getAttribute("data-modal"),
        modalElem = document.querySelector(
          '.modal[data-modal="' + modalId + '"]'
        );

      /* После того как нашли нужное модальное окно, добавим классы
            подложке и окну чтобы показать их. */
      modalElem.classList.add("active");
      overlay.classList.add("active");
    }); // end click
  }); // end foreach

  closeButtons.forEach(function(item) {
    item.addEventListener("click", function(e) {
      var parentModal = this.closest(".modal");

      parentModal.classList.remove("active");
      overlay.classList.remove("active");
    });
  }); // end foreach

  document.body.addEventListener(
    "keyup",
    function(e) {
      var key = e.keyCode;

      if (key == 27) {
        document.querySelector(".modal.active").classList.remove("active");
        document.querySelector(".overlay").classList.remove("active");
      }
    },
    false
  );

  overlay.addEventListener("click", function() {
    document.querySelector(".modal.active").classList.remove("active");
    this.classList.remove("active");
  });
}); // end ready

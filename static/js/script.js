window.onload = load;

function load() {
  let btnToggle = document.querySelector(".button_slide");
  let sidebar = document.querySelector(".sidebar");
  let sidebar_menu = document.querySelector(".sidebar_menu");

  sidebar_menu.classList.add("hidden");

  btnToggle.addEventListener("click", (e) => {
    sidebar.classList.toggle("active");
    sidebar_menu.classList.toggle("hidden");
  });
}


$(document).ready(function() {
  $('.menu').click(function() {
    $(this).find('.dropdown').slideToggle('fast');
  });

  $('.dropdown').hide();
});

var btn = document.getElementById("theme-button");
var link = document.getElementById("theme-link");
var switchToggle = document.querySelector(".switch.switch200 input[type='checkbox']");

switchToggle.addEventListener("click", function () {
  ChangeTheme();
});
function ChangeTheme()
{
    let lightTheme = "{% static 'css/light.css' %}";
    let darkTheme = "{% static 'css/dark.css' %}";

    var currTheme = link.getAttribute("href");
    var theme = "";

    if(currTheme == lightTheme)
    {
   	 currTheme = darkTheme;
   	 theme = "dark";
    }
    else
    {    
   	 currTheme = lightTheme;
   	 theme = "light";
    }

    link.setAttribute("href", currTheme);

    Save(theme);
}
/*
 * CourseForge — barra de abas do topo (um curso por aba).
 *
 * Com muitos cursos, as abas não cabem na tela e a lista fica cortada. O tema
 * já deixa a lista rolar para o lado, mas só com trackpad ou Shift+rodinha.
 * Este script acrescenta:
 *   - setas ‹ › nas pontas, que só aparecem quando há abas escondidas daquele lado;
 *   - rodinha do mouse rolando para o lado em cima da barra;
 *   - arrastar com o mouse (no celular, o dedo já arrasta);
 *   - a aba da página atual aparece ao abrir (não fica escondida no fim).
 */
(function () {
  "use strict";

  function iniciar() {
    var lista = document.querySelector(".md-tabs__list");
    if (!lista || lista.dataset.cfAbas) return;
    lista.dataset.cfAbas = "sim";
    var barra = lista.parentElement;  // .md-grid
    barra.classList.add("cf-abas");

    function seta(classe, rotulo, texto, sentido) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "cf-abas__seta " + classe;
      b.setAttribute("aria-label", rotulo);
      b.textContent = texto;
      b.addEventListener("click", function () {
        lista.scrollBy({ left: sentido * lista.clientWidth * 0.6, behavior: "smooth" });
      });
      barra.appendChild(b);
      return b;
    }
    var esquerda = seta("cf-abas__seta--esquerda", "Mostrar abas anteriores", "‹", -1);
    var direita = seta("cf-abas__seta--direita", "Mostrar mais abas", "›", 1);

    function atualizar() {
      var sobra = lista.scrollWidth - lista.clientWidth;
      barra.classList.toggle("cf-abas--inicio", lista.scrollLeft > 2);
      barra.classList.toggle("cf-abas--fim", sobra > 2 && lista.scrollLeft < sobra - 2);
      esquerda.hidden = !(lista.scrollLeft > 2);
      direita.hidden = !(sobra > 2 && lista.scrollLeft < sobra - 2);
    }

    // Rodinha do mouse: em cima da barra, rola para o lado
    lista.addEventListener("wheel", function (e) {
      if (Math.abs(e.deltaY) <= Math.abs(e.deltaX)) return;  // trackpad já rola para o lado
      var sobra = lista.scrollWidth - lista.clientWidth;
      var podeRolar = (e.deltaY > 0 && lista.scrollLeft < sobra) || (e.deltaY < 0 && lista.scrollLeft > 0);
      if (!podeRolar) return;  // no fim da barra, a rodinha volta a rolar a página
      e.preventDefault();
      lista.scrollLeft += e.deltaY;
    }, { passive: false });

    // Arrastar com o mouse (toque e caneta o navegador já trata)
    var inicioX = null, inicioScroll = 0, arrastou = false;
    lista.addEventListener("pointerdown", function (e) {
      if (e.pointerType !== "mouse" || e.button !== 0) return;
      inicioX = e.clientX;
      inicioScroll = lista.scrollLeft;
      arrastou = false;
    });
    window.addEventListener("pointermove", function (e) {
      if (inicioX === null) return;
      var dx = e.clientX - inicioX;
      if (Math.abs(dx) > 5) {
        arrastou = true;
        barra.classList.add("cf-abas--arrastando");
      }
      if (arrastou) lista.scrollLeft = inicioScroll - dx;
    });
    window.addEventListener("pointerup", function () {
      inicioX = null;
      barra.classList.remove("cf-abas--arrastando");
    });
    // O clique que termina um arrasto não abre a aba
    lista.addEventListener("click", function (e) {
      if (arrastou) { e.preventDefault(); e.stopPropagation(); arrastou = false; }
    }, true);
    lista.addEventListener("dragstart", function (e) { e.preventDefault(); });

    lista.addEventListener("scroll", atualizar, { passive: true });
    window.addEventListener("resize", atualizar);

    // A aba da página atual aparece ao abrir
    var ativa = lista.querySelector(".md-tabs__item--active");
    if (ativa) {
      var deslocamento = ativa.getBoundingClientRect().left - lista.getBoundingClientRect().left + lista.scrollLeft;
      var centro = deslocamento - (lista.clientWidth - ativa.offsetWidth) / 2;
      lista.style.scrollBehavior = "auto";  // ao abrir, sem animação
      lista.scrollLeft = Math.max(0, centro);
      lista.style.scrollBehavior = "";
    }
    atualizar();
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(iniciar);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciar);
  } else {
    iniciar();
  }
})();

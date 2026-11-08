/*
 * CourseForge — slider do banner da página inicial.
 *
 * O HTML (cursos/index.md) já funciona sem este arquivo: os slides ficam numa
 * faixa que rola para o lado. Este script acrescenta setas, bolinhas, a troca
 * automática e um botão de pausa. A troca automática para só quando a pessoa
 * aperta a pausa ou navega com o teclado dentro do banner (o mouse em cima não
 * pausa: era justamente quando a pessoa estava olhando). Quem prefere menos
 * movimento no sistema continua vendo a troca, mas sem a animação de deslizar.
 */
(function () {
  "use strict";

  var INTERVALO_MS = 7000;

  function iniciar(slider) {
    var trilho = slider.querySelector(".cf-slider__trilho");
    var slides = trilho ? Array.prototype.slice.call(trilho.querySelectorAll(".cf-slide")) : [];
    if (slides.length < 2 || slider.dataset.cfIniciado) return;
    slider.dataset.cfIniciado = "sim";

    var reduzirMovimento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var atual = 0;
    var timer = null;
    var pausadoPeloUsuario = false;
    var focoTeclado = false;

    function criarBotao(classe, rotulo, texto) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = classe;
      b.setAttribute("aria-label", rotulo);
      if (texto) b.textContent = texto;
      return b;
    }

    var controles = document.createElement("div");
    controles.className = "cf-slider__controles";
    var anterior = criarBotao("cf-slider__seta", "Slide anterior", "‹");
    var proximo = criarBotao("cf-slider__seta", "Próximo slide", "›");
    var pontos = document.createElement("div");
    pontos.className = "cf-slider__pontos";
    var pausa = criarBotao("cf-slider__seta cf-slider__pausa", "", "");

    var botoesPonto = slides.map(function (slide, i) {
      var nome = slide.querySelector(".cf-hero__eyebrow");
      var rotulo = "Ir para o slide " + (i + 1) + (nome ? ": " + nome.textContent.trim() : "");
      var p = criarBotao("cf-slider__ponto", rotulo);
      p.addEventListener("click", function () { irPara(i); });
      pontos.appendChild(p);
      return p;
    });

    controles.appendChild(anterior);
    controles.appendChild(pontos);
    controles.appendChild(proximo);
    controles.appendChild(pausa);
    slider.appendChild(controles);

    function marcar(i) {
      atual = i;
      botoesPonto.forEach(function (p, j) {
        p.setAttribute("aria-current", j === i ? "true" : "false");
      });
      slides.forEach(function (s, j) {
        // Só o slide visível entra na ordem do Tab e no leitor de tela
        if (j === i) {
          s.removeAttribute("aria-hidden");
          s.removeAttribute("inert");
        } else {
          s.setAttribute("aria-hidden", "true");
          s.setAttribute("inert", "");
        }
      });
    }

    function irPara(i) {
      var total = slides.length;
      i = ((i % total) + total) % total;
      trilho.scrollTo({ left: slides[i].offsetLeft - trilho.offsetLeft, behavior: reduzirMovimento ? "auto" : "smooth" });
      marcar(i);
    }

    function atualizarPausa() {
      var parado = pausadoPeloUsuario;
      pausa.textContent = parado ? "▶" : "❚❚";
      pausa.setAttribute("aria-label", parado ? "Retomar a troca automática" : "Pausar a troca automática");
      pausa.setAttribute("aria-pressed", parado ? "true" : "false");
    }

    function agendar() {
      clearInterval(timer);
      timer = null;
      if (pausadoPeloUsuario || focoTeclado || document.hidden) return;
      timer = setInterval(function () { irPara(atual + 1); }, INTERVALO_MS);
    }

    anterior.addEventListener("click", function () { irPara(atual - 1); agendar(); });
    proximo.addEventListener("click", function () { irPara(atual + 1); agendar(); });
    pausa.addEventListener("click", function () {
      pausadoPeloUsuario = !pausadoPeloUsuario;
      atualizarPausa();
      agendar();
    });

    // Pausa enquanto o foco do TECLADO estiver no banner (clique de mouse não conta)
    slider.addEventListener("focusin", function (e) {
      var alvo = e.target;
      focoTeclado = alvo && alvo.matches && alvo.matches(":focus-visible");
      agendar();
    });
    slider.addEventListener("focusout", function (e) {
      if (!slider.contains(e.relatedTarget)) { focoTeclado = false; agendar(); }
    });
    document.addEventListener("visibilitychange", agendar);

    trilho.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); irPara(atual + 1); }
      if (e.key === "ArrowLeft") { e.preventDefault(); irPara(atual - 1); }
    });

    // Se a pessoa arrastar a faixa (toque no celular), acompanha o slide visível
    var espera = null;
    trilho.addEventListener("scroll", function () {
      clearTimeout(espera);
      espera = setTimeout(function () {
        var i = Math.round(trilho.scrollLeft / trilho.clientWidth);
        if (i !== atual && i >= 0 && i < slides.length) marcar(i);
      }, 120);
    }, { passive: true });

    marcar(0);
    atualizarPausa();
    agendar();
  }

  function iniciarTodos() {
    var sliders = document.querySelectorAll("[data-cf-slider]");
    Array.prototype.forEach.call(sliders, iniciar);
  }

  // Compatível com a navegação instantânea do Material (document$), se for ligada no futuro
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(iniciarTodos);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", iniciarTodos);
  } else {
    iniciarTodos();
  }
})();

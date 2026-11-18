/* ==========================================================================
   Teach · Interactive Engine (Theme, Drawer, Persistence, Router, Quiz, Handback)
   ========================================================================== */

(function () {
  "use strict";

  var lessonKey = document.body.dataset.lessonId || "ai-software-factory/lesson-0001";
  var state = {
    routerPassed: 0,
    routerTotal: 0,
    quizCorrect: 0,
    quizTotal: 0,
    quizMissed: [],
    notes: ""
  };

  function storageKey(suffix) {
    return "teach::" + lessonKey + "::" + suffix;
  }

  function buildHandbackPayload() {
    var parts = lessonKey.split("/");
    var course = parts[0] || "ai-software-factory";
    var lesson = parts[1] || "0001";
    var body = [
      "/teach session-handback",
      "Course: " + course + " | Lesson: " + lesson,
      "Router: " + state.routerPassed + "/" + state.routerTotal +
        " | Quiz: " + state.quizCorrect + "/" + state.quizTotal +
        " | Missed: " + (state.quizMissed.length ? state.quizMissed.join(", ") : "None"),
      "Follow-up Notes: " + (state.notes.trim() || "None — ready for Lesson 0002")
    ].join("\n");
    return {
      course: course,
      lesson: lesson,
      body: body
    };
  }

  function updateHandbackUI() {
    var railEl = document.getElementById("railScore");
    var summaryEl = document.querySelector("[data-handback-summary]");
    var issueLink = document.querySelector("[data-issue-handback]");
    if (railEl && state.quizTotal > 0) {
      railEl.textContent = "Quiz: " + state.quizCorrect + " / " + state.quizTotal +
        (state.routerTotal > 0 ? " · Router: " + state.routerPassed + " / " + state.routerTotal : "");
    }
    if (summaryEl) {
      var parts = [];
      if (state.routerTotal > 0) parts.push("Router " + state.routerPassed + "/" + state.routerTotal);
      if (state.quizTotal > 0) parts.push("Quiz " + state.quizCorrect + "/" + state.quizTotal);
      if (state.notes.trim()) parts.push("Follow-up notes ready");
      summaryEl.textContent = parts.length ? parts.join(" · ") : "Complete exercises above to build your handback.";
    }
    if (issueLink) {
      var payload = buildHandbackPayload();
      var title = "[teach] " + payload.course + " · " + payload.lesson + " handback";
      issueLink.href = "https://github.com/GCherry/teach/issues/new?title=" +
        encodeURIComponent(title) + "&body=" + encodeURIComponent(payload.body);
    }
  }

  function initTheme() {
    var btn = document.querySelector("[data-theme-toggle]");
    var badge = document.querySelector("[data-mode-badge]");

    function sync() {
      var cur = document.documentElement.getAttribute("data-theme") || "dark";
      if (btn) btn.textContent = cur === "light" ? "Dark Mode" : "Light Mode";
      if (badge) badge.textContent = cur === "light" ? "Light Mode" : "Dark Mode";
    }

    if (btn) {
      btn.addEventListener("click", function () {
        var cur = document.documentElement.getAttribute("data-theme") || "dark";
        var next = cur === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        try { localStorage.setItem("teach_theme", next); } catch (_) {}
        sync();
      });
    }
    sync();
  }

  function initDrawer() {
    var drawer = document.getElementById("refDrawer");
    var openBtn = document.querySelector("[data-drawer-toggle]");
    var closeBtn = document.querySelector("[data-drawer-close]");
    if (!drawer) return;

    if (openBtn) {
      openBtn.addEventListener("click", function () { drawer.classList.toggle("open"); });
    }
    if (closeBtn) {
      closeBtn.addEventListener("click", function () { drawer.classList.remove("open"); });
    }
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") drawer.classList.remove("open");
    });
  }

  function initQuizzes() {
    document.querySelectorAll("[data-quiz]").forEach(function (quizEl) {
      var questions = Array.from(quizEl.querySelectorAll("[data-question]"));
      var scoreEl = quizEl.querySelector("[data-quiz-score]");
      var resetBtn = quizEl.querySelector("[data-quiz-reset]");
      state.quizTotal = questions.length;

      function saveQuiz() {
        var saved = questions.map(function (q) {
          return q.dataset.chosenIndex !== undefined ? Number(q.dataset.chosenIndex) : null;
        });
        try { localStorage.setItem(storageKey("quiz"), JSON.stringify(saved)); } catch (_) {}
      }

      function updateScore() {
        var answered = questions.filter(function (q) { return q.dataset.state === "answered"; }).length;
        var correct = questions.filter(function (q) { return q.dataset.result === "correct"; }).length;
        state.quizCorrect = correct;
        state.quizMissed = questions
          .map(function (q, idx) { return q.dataset.result === "wrong" ? "Q" + (idx + 1) : null; })
          .filter(Boolean);
        if (scoreEl) {
          scoreEl.textContent = "Score: " + correct + " / " + questions.length +
            (answered < questions.length ? " (" + answered + " answered)" : " (Complete)");
        }
        updateHandbackUI();
      }

      function applySelection(qEl, options, idx) {
        var btn = options[idx];
        if (!btn) return;
        qEl.dataset.state = "answered";
        qEl.dataset.chosenIndex = String(idx);
        var isCorrect = btn.dataset.correct === "true";
        qEl.dataset.result = isCorrect ? "correct" : "wrong";

        options.forEach(function (opt) {
          opt.disabled = true;
          if (opt.dataset.correct === "true") opt.classList.add("is-correct");
          else if (opt === btn && !isCorrect) opt.classList.add("is-wrong");
        });

        var rationaleEl = qEl.querySelector(".quiz-rationale");
        if (rationaleEl) {
          rationaleEl.textContent = (isCorrect ? "Correct — " : "Not quite — ") +
            (btn.dataset.rationale || qEl.dataset.explanation || "");
          rationaleEl.classList.add("is-visible");
        }
      }

      questions.forEach(function (qEl) {
        var options = Array.from(qEl.querySelectorAll(".quiz-option"));
        options.forEach(function (btn, idx) {
          btn.addEventListener("click", function () {
            if (qEl.dataset.state === "answered") return;
            applySelection(qEl, options, idx);
            saveQuiz();
            updateScore();
          });
        });
      });

      try {
        var restored = JSON.parse(localStorage.getItem(storageKey("quiz")) || "null");
        if (Array.isArray(restored)) {
          restored.forEach(function (chosen, qIdx) {
            if (chosen !== null && questions[qIdx]) {
              applySelection(questions[qIdx], Array.from(questions[qIdx].querySelectorAll(".quiz-option")), chosen);
            }
          });
        }
      } catch (_) {}

      if (resetBtn) {
        resetBtn.addEventListener("click", function () {
          questions.forEach(function (qEl) {
            delete qEl.dataset.state;
            delete qEl.dataset.result;
            delete qEl.dataset.chosenIndex;
            qEl.querySelectorAll(".quiz-option").forEach(function (opt) {
              opt.disabled = false;
              opt.classList.remove("is-correct", "is-wrong");
            });
            var rationaleEl = qEl.querySelector(".quiz-rationale");
            if (rationaleEl) {
              rationaleEl.textContent = "";
              rationaleEl.classList.remove("is-visible");
            }
          });
          try { localStorage.removeItem(storageKey("quiz")); } catch (_) {}
          updateScore();
        });
      }

      updateScore();
    });
  }

  function initRouters() {
    document.querySelectorAll("[data-router-exercise]").forEach(function (box) {
      var rows = Array.from(box.querySelectorAll("[data-scenario]"));
      var scoreEl = box.querySelector("[data-router-score]");
      var checkBtn = box.querySelector("[data-router-check]");
      var resetBtn = box.querySelector("[data-router-reset]");
      state.routerTotal = rows.length;

      function saveRouter() {
        var data = rows.map(function (r) {
          return Array.from(r.querySelectorAll("select")).map(function (s) { return s.value; });
        });
        try { localStorage.setItem(storageKey("router"), JSON.stringify(data)); } catch (_) {}
      }

      function evaluate() {
        var passed = 0;
        rows.forEach(function (row) {
          var selects = Array.from(row.querySelectorAll("select[data-expected]"));
          var feedback = row.querySelector(".scenario-feedback");
          var allSelected = selects.every(function (s) { return s.value !== ""; });
          var allRight = selects.every(function (s) { return s.value === s.dataset.expected; });

          if (!allSelected) {
            if (feedback) {
              feedback.className = "scenario-feedback is-bad";
              feedback.textContent = "Select an option in every dropdown before checking.";
            }
            return;
          }

          if (allRight) {
            passed += 1;
            if (feedback) {
              feedback.className = "scenario-feedback is-ok";
              feedback.textContent = "Exact match — " + (row.dataset.okNote || "");
            }
          } else {
            var hints = selects
              .filter(function (s) { return s.value !== s.dataset.expected; })
              .map(function (s) { return s.dataset.hint; })
              .filter(Boolean);
            if (feedback) {
              feedback.className = "scenario-feedback is-bad";
              feedback.textContent = "Adjust routing: " + hints.join(" ");
            }
          }
        });

        state.routerPassed = passed;
        if (scoreEl) scoreEl.textContent = "Routed: " + passed + " / " + rows.length;
        saveRouter();
        updateHandbackUI();
      }

      try {
        var restored = JSON.parse(localStorage.getItem(storageKey("router")) || "null");
        if (Array.isArray(restored)) {
          restored.forEach(function (vals, idx) {
            if (!rows[idx]) return;
            var selects = Array.from(rows[idx].querySelectorAll("select"));
            selects.forEach(function (s, sIdx) {
              if (typeof vals[sIdx] === "string") s.value = vals[sIdx];
            });
          });
          if (restored.some(function (vals) { return vals.some(Boolean); })) evaluate();
        }
      } catch (_) {}

      if (checkBtn) checkBtn.addEventListener("click", evaluate);

      if (resetBtn) {
        resetBtn.addEventListener("click", function () {
          rows.forEach(function (row) {
            row.querySelectorAll("select[data-expected]").forEach(function (s) { s.value = ""; });
            var feedback = row.querySelector(".scenario-feedback");
            if (feedback) {
              feedback.className = "scenario-feedback";
              feedback.textContent = "";
            }
          });
          state.routerPassed = 0;
          if (scoreEl) scoreEl.textContent = "Routed: 0 / " + rows.length;
          try { localStorage.removeItem(storageKey("router")); } catch (_) {}
          updateHandbackUI();
        });
      }
    });
  }

  function initHandback() {
    var notesEl = document.querySelector("[data-handback-notes]");
    var copyBtn = document.querySelector("[data-copy-handback]");

    if (notesEl) {
      try {
        var saved = localStorage.getItem(storageKey("notes")) || "";
        notesEl.value = saved;
        state.notes = saved;
      } catch (_) {}
      notesEl.addEventListener("input", function () {
        state.notes = notesEl.value;
        try { localStorage.setItem(storageKey("notes"), state.notes); } catch (_) {}
        updateHandbackUI();
      });
    }

    if (copyBtn) {
      copyBtn.addEventListener("click", function () {
        var payload = buildHandbackPayload().body;
        if (navigator.clipboard) navigator.clipboard.writeText(payload);
        var original = copyBtn.textContent;
        copyBtn.textContent = "Copied Handback!";
        setTimeout(function () { copyBtn.textContent = original; }, 1800);
      });
    }
    updateHandbackUI();
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTheme();
    initDrawer();
    initRouters();
    initQuizzes();
    initHandback();
  });
})();

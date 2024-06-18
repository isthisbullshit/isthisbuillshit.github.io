const main = () => {
  const _elements = {
    checkBtn: document.getElementById("check"),
    checkAgainBtn: document.getElementById("check-again"),
    input: document.getElementById("input"),
    loading: document.getElementById("loading"),
    bsQuery: document.getElementById("bs-query"),
    bsReport: document.getElementById("bs-report"),
    bsScore: document.getElementById("bs-score"),
    bsSummary: document.getElementById("bs-summary"),
    bsFactors: document.getElementById("bs-factors"),
    bsShare: document.getElementById("bs-share"),
  };

  const aiServices = [
    "Checking ChatGPT v5...",
    "Checking Gemini...",
    "Querying blockchains...",
    "Connecting to Starlink...",
    "Pinging Elon Musk...",
    "AI is thinking...",
  ];

  const bsFactors = [
    "Human Error",
    "AI Limitations",
    "Quantum interference",
    "Murphys Law",
    "Heisenberg Uncertainty Principle",
    "Schrodingers Cat",
    "The Butterfly Effect",
    "Confirmation Bias",
    "Anecdotal Evidence",
    "Fabrication",
    "Absence of Peer Review",
    "Memory Distortion",
    "Instrumentation Errors",
    "Temporal Confounding",
    "Propaganda",
    "Statistical Variability",
    "Misinterpretation",
  ];

  const placeholders = [
    "The earth is flat.",
    "Butterflies are government drones.",
    "The moon landing was fake.",
    "Light bulbs are sentient.",
    "The sun is a hologram.",
    "The ocean is a simulation.",
    "The sky is a painting.",
    "The grass is a lie.",
    "The trees are listening.",
    "The government is ran by liazard people.",
    "The government is ran by aliens.",
    "Aliens are among us.",
    "Bullshit is everywhere.",
    "Jokes are real.",
    "Flat earthers are right.",
    "Speed of light is not constant.",
    "The wind is really the trees farting.",
    "Shooting stars are really aliens crashing.",
    "Eating vegetables is bad for you.",
    "Eat too many vegetables and you will turn into a vegetable.",
    "Black holes are really the universe's belly button.",
    "Cats are actually secret agents from an unknown civilization.",
    "The cake is a lie.",
    "We are all living in a simulation.",
  ];
  const placeholder =
    placeholders[Math.floor(Math.random() * placeholders.length)];
  _elements.input.placeholder = `Example: ${placeholder}`;

  const urlParams = new URLSearchParams(window.location.search);
  const initialBsQuery = urlParams.get("bs-query");
  if (initialBsQuery) {
    _elements.input.value = initialBsQuery;
  }

  _elements.checkBtn.addEventListener("click", () => {
    const inputValue = _elements.input.value;
    if (inputValue === "") {
      window.alert("You need to enter something to be checked for bullshit");
      return;
    }
    if (inputValue.length > 1000) {
      window.alert(
        `Due to AI constraints, on our free tier the bullshit query must be less than 1000 characters (current query characters: ${inputValue.length}).`,
      );
      return;
    }

    setBsUrlQuery(inputValue);

    _elements.loading.style.display = "block";
    _elements.bsReport.style.display = "none";
    _elements.checkBtn.disabled = true;
    _elements.input.disabled = true;

    const stopAiQuery = startAiQuery();
    const { score, summary, factors } = bullshitReport(inputValue);
    setTimeout(() => {
      _elements.loading.style.display = "none";
      _elements.bsReport.style.display = "block";
      _elements.bsQuery.style.display = "none";
      _elements.bsScore.innerText = score;
      _elements.bsSummary.innerText = summary;
      _elements.bsFactors.innerText = factors.join(", ");
      _elements.checkBtn.disabled = false;
      _elements.input.disabled = false;
      stopAiQuery();
    }, 8000);
  });

  _elements.checkAgainBtn.addEventListener("click", () => {
    setBsUrlQuery("");
    _elements.input.value = "";
    _elements.bsQuery.style.display = "block";
    _elements.bsReport.style.display = "none";
  });

  _elements.bsShare.addEventListener("click", () => {
    const report = window.location.href;
    if (!navigator.share) {
      btnText = _elements.bsShare.innerText;
      navigator.clipboard.writeText(report);
      _elements.bsShare.innerText = "Copied!";
      setTimeout(() => {
        _elements.bsShare.innerText = btnText;
      }, 2000);
      return;
    }
    navigator.share(report).catch((err) => {
      console.error(err);
    });
  });

  const startAiQuery = () => {
    let i = 0;
    _elements.loading.innerText = aiServices[i];

    const interval = setInterval(() => {
      i++;
      _elements.loading.innerText = aiServices[i % aiServices.length];
    }, 1500);
    return () => {
      clearInterval(interval);
    };
  };

  const setBsUrlQuery = (query) => {
    const url = new URL(window.location.href);
    url.searchParams.set("bs-query", query);
    window.history.replaceState({}, "", url);
  };

  const encoder = new TextEncoder();
  const bullshitReport = (str) => {
    const uint = encoder.encode(str);
    let total = 0;
    uint.forEach((byte) => {
      total += byte;
    });
    const score = total % 100;

    const summary = scoreToSummary(score);
    const factors = factorsFromScore(score);
    return { score, summary, factors };
  };

  const scoreToSummary = (score) => {
    if (score < 10) {
      return "Very low bullshit detected";
    }
    if (score < 30) {
      return "Low bullshit detected";
    }
    if (score < 60) {
      return "Medium bullshit detected";
    }
    if (score < 80) {
      return "High bullshit detected, caution advised";
    }
    return "Very high bullshit detected, proceed with caution";
  };
  const factorsFromScore = (score) => {
    const factors = [];
    bsFactors.forEach((factor, i) => {
      if ((score / (i + 1 * 2.8)) % 2 > 1.7) {
        factors.push(factor);
      }
    });
    if (factors.length === 0) {
      factors.push("No factors detected");
    }
    // Return only top 3 factors
    return factors.slice(0, 3);
  };
};
main();

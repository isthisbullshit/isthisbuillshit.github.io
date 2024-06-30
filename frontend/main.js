const main = () => {
  const aiEngineVersion = "v3.14.1592";
  const queryLimitFreeTier = 1500;

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
    bsCertify: document.getElementById("bs-certify"),
    bsExonerate: document.getElementById("bs-exonerate"),
    aiVersion: document.getElementById("ai-version"),
  };

  const aiServices = [
    "Checking ChatGPT v5...",
    "Checking Gemini...",
    "Querying blockchains...",
    "Connecting to Starlink...",
    "Pinging Elon Musk...",
    "Checking Neuralink...",
  ];

  const bsFactors = [
    "Human Error",
    "AI Limitations",
    "Quantum Interference",
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
    "Misrepresentation",
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

  const event = {
    view: "page-view",
    query: "bs-query",
    share: "bs-share",
    certify: "bs-certify",
    exonerate: "bs-exonerate",
    emptyRequest: "bs-empty",
    limitFreeTier: "bs-limitFreeTier",
  };

  const onInit = () => {
    _elements.aiVersion.innerText = aiEngineVersion;
    setRandomPlaceholder();

    const urlParams = new URLSearchParams(window.location.search);
    const initialBsQuery = urlParams.get("bs-query");
    if (initialBsQuery) {
      _elements.input.value = initialBsQuery;
    }
    bsTrack(event.view, initialBsQuery);
  };

  _elements.checkBtn.addEventListener("click", () => {
    const inputValue = _elements.input.value;
    if (inputValue === "") {
      bsTrack(event.emptyRequest);
      window.alert("You need to enter something to be checked for bullshit");
      return;
    }
    if (inputValue.length > queryLimitFreeTier) {
      bsTrack(event.limitFreeTier);
      window.alert(
        `Due to AI constraints, on our free tier the bullshit query must be less than ${queryLimitFreeTier} characters (current query characters: ${inputValue.length}).`,
      );
      return;
    }

    setBsUrlQuery(inputValue);

    _elements.loading.style.display = "block";
    _elements.bsReport.style.display = "none";
    _elements.checkBtn.disabled = true;
    _elements.input.disabled = true;

    const stopAiQuery = startAiQuery();
    const report = newBullshitRepot(inputValue);
    bsTrack(event.query, { query: inputValue, report });

    setTimeout(() => {
      _elements.loading.style.display = "none";
      _elements.bsReport.style.display = "block";
      _elements.bsQuery.style.display = "none";
      _elements.bsScore.innerText = report.score;
      _elements.bsSummary.innerText = report.summary;
      _elements.bsFactors.innerText = report.factors.join(", ");
      _elements.checkBtn.disabled = false;
      _elements.input.disabled = false;
      stopAiQuery();
    }, 7000);
  });

  _elements.checkAgainBtn.addEventListener("click", () => {
    setRandomPlaceholder();
    setBsUrlQuery("");
    _elements.input.value = "";
    _elements.bsQuery.style.display = "block";
    _elements.bsReport.style.display = "none";
  });

  _elements.bsShare.addEventListener("click", () => {
    bsTrack(event.share);
    const report = window.location.href;
    if (navigator.share) {
      const data = {
        title: "Bullshit Report",
        text: "Check out this bullshit report",
        url: report,
      };
      navigator.share(data).catch((err) => {
        console.error(err);
      });
      return;
    }

    // Fallback to clipboard
    if (_elements.bsShare.dataset.copied === "true") {
      return;
    }
    const btnText = _elements.bsShare.innerText;
    navigator.clipboard.writeText(report);
    _elements.bsShare.innerText = "Copied report!";
    _elements.bsShare.dataset.copied = "true";
    setTimeout(() => {
      _elements.bsShare.innerText = btnText;
      _elements.bsShare.dataset.copied = "done";
    }, 2000);
  });

  _elements.bsCertify.addEventListener("click", () => {
    bsTrack(event.certify);
    const url = new URL(window.location.href);
    url.searchParams.set("bs-verdict","certified-bs");
    url.pathname = url.pathname.replace("/index.html","/verdict.html")
    window.location.href = url.href;
  });

  _elements.bsExonerate.addEventListener("click", () => {
    bsTrack(event.certify);
    const url = new URL(window.location.href);
    url.searchParams.set("bs-verdict","true-face");
    url.pathname = url.pathname.replace("/index.html","/verdict.html")
    window.location.href = url.href;
  });

  const setRandomPlaceholder = () => {
    const placeholder =
      placeholders[Math.floor(Math.random() * placeholders.length)];
    _elements.input.placeholder = `Example: ${placeholder}`;
  };

  const startAiQuery = () => {
    let i = 0;
    _elements.loading.innerText = aiServices[i];

    const interval = setInterval(() => {
      i++;
      _elements.loading.innerText = aiServices[i % aiServices.length];
    }, 1300);
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
  const newBullshitRepot = (str) => {
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
    if (score < 70) {
      return "Medium bullshit detected";
    }
    if (score < 85) {
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
    return factors.slice(0, 3);
  };

  const bsTrack = (event, data) => {
    const apiUrl = `${window.location.protocol}//api.${window.location.host}/metrics`;
    const headers = new Headers();
    headers.append("Content-Type", "application/json");

    const body = {
      type: event,
      data: data ?? null,
    };

    const requestOptions = {
      method: "POST",
      headers: headers,
      body: JSON.stringify(body),
      credentials: "include",
    };

    fetch(apiUrl, requestOptions).catch((err) => {
      console.warn(err);
    });
  };

  onInit();
};
main();

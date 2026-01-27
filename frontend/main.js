const main = () => {
  const aiEngineVersion = "v3.14.1592";
  const queryLimitFreeTier = 1500;

  const _elements = {
    loginBtn: document.getElementById("login"),
    loginStatus: document.getElementById("login-status"),
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
    bsQueryText: document.getElementById("bs-query-text"),
    certified_bs_stamp: document.getElementById("certified-bs-stamp"),
    true_fact_stamp: document.getElementById("true-fact-stamp"),
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
    view_query: "view-query",
    query: "bs-query",
    view_report: "view-report",
    share: "bs-share",
    certify: "bs-certify",
    exonerate: "bs-exonerate",
    emptyRequest: "bs-empty",
    limitFreeTier: "bs-limitFreeTier",
  };

  const onInit = () => {
    _elements.aiVersion.innerText = aiEngineVersion;
    setRandomPlaceholder();
    loadLoginStatus();

    const urlParams = new URLSearchParams(window.location.search);
    const initialBsQuery = urlParams.get("bs-query");
    const initialBSReport = urlParams.get("bs-report");
    const certification = urlParams.get("bs-certified");

    if (initialBsQuery) {
      _elements.input.value = initialBsQuery;
      bsTrack(event.view_query, initialBsQuery);
    } else if (initialBSReport){
      const the_report = newBullshitRepot(initialBSReport);
      displayReport(the_report);
      bsTrack(event.view_report, initialBSReport);
      if (certification) {
        setVerdictView(certification)
      }
    } else {
      bsTrack(event.view, initialBsQuery);
    }
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
      setBsUrlReport(inputValue);
      displayReport(report);
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
    setVerdict(event.certify);
  });

  _elements.bsExonerate.addEventListener("click", () => {
    setVerdict(event.exonerate);
  });

  _elements.loginBtn?.addEventListener("click", async () => {
    _elements.loginBtn.disabled = true;
    const originalText = _elements.loginBtn.innerText;
    const isLoggedIn = _elements.loginBtn.dataset.loggedIn === "true";
    _elements.loginBtn.innerText = isLoggedIn ? "Logging out..." : "Logging in...";

    try {
      const endpoint = isLoggedIn ? "/api/auth/logout" : "/api/auth/login";
      const response = await fetch(endpoint, {
        method: "POST",
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error(`Login failed with status ${response.status}`);
      }
      await loadLoginStatus();
    } catch (err) {
      console.warn(err);
      _elements.loginBtn.innerText = originalText;
      _elements.loginBtn.disabled = false;
      window.alert("Login failed. Please try again.");
    }
  });

  const loadLoginStatus = async () => {
    if (!_elements.loginStatus) {
      return;
    }

    try {
      const response = await fetch("/api/auth/status", {
        method: "GET",
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error(`Status failed with ${response.status}`);
      }
      const data = await response.json();
      setLoginUi(Boolean(data.logged_in));
    } catch (err) {
      console.warn(err);
      _elements.loginStatus.innerText = "Status: unknown";
      if (_elements.loginBtn) {
        _elements.loginBtn.dataset.loggedIn = "false";
        _elements.loginBtn.innerText = "Login";
      }
    }
  };

  const setLoginUi = (loggedIn) => {
    if (_elements.loginStatus) {
      _elements.loginStatus.innerText = loggedIn
        ? "Status: logged in"
        : "Status: logged out";
    }
    if (_elements.loginBtn) {
      _elements.loginBtn.dataset.loggedIn = loggedIn ? "true" : "false";
      _elements.loginBtn.innerText = loggedIn ? "Log out" : "Login";
      _elements.loginBtn.disabled = false;
    }
  };


  const displayReport = (report) => {
    _elements.loading.style.display = "none";
    _elements.bsReport.style.display = "block";
    _elements.bsQuery.style.display = "none";
    _elements.bsQueryText.innerText = report.query_string;
    _elements.bsScore.innerText = report.score;
    _elements.bsSummary.innerText = report.summary;
    _elements.bsFactors.innerText = report.factors.join(", ");
    _elements.checkBtn.disabled = false;
    _elements.input.disabled = false;
  }

  const  setVerdict = (verdictEvent) => {
    const url = new URL(window.location.href);
    bsTrack(verdictEvent, {query: url.searchParams.get("bs-report")});
    url.searchParams.set("bs-certified", verdictEvent);
    setVerdictView(verdictEvent);
    window.history.replaceState({}, "", url);
  }

  const setVerdictView = (verdictEvent) => {
    if (verdictEvent === event.certify) {
      _elements.true_fact_stamp.style.display = "none"
      _elements.certified_bs_stamp.style.display = "block"
    } else if (verdictEvent === event.exonerate) {
      _elements.true_fact_stamp.style.display = "block"
      _elements.certified_bs_stamp.style.display = "none"
    } else {
      _elements.true_fact_stamp.style.display = "none"
      _elements.certified_bs_stamp.style.display = "none"
    }
  }

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

  const setBsUrlReport = (query) => {
    const url = new URL(window.location.href);
    url.searchParams.delete("bs-query");
    url.searchParams.set("bs-report", query);
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
    const query_string = str
    return { score, summary, factors, query_string};
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
    const apiUrl = `${location.protocol}//${
      location.hostname === 'localhost' || location.hostname.startsWith('api') ? location.host : `api.${location.host}`
    }/metrics`;
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

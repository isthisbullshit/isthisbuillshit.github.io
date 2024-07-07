const main = () => {
  const _elements = {
    the_bullshit: document.getElementById("the-bullshit"),
    true_fact_stamp: document.getElementById("true-fact-stamp"),
    certified_bs_stamp: document.getElementById("certified-bs-stamp"),
    date: document.getElementById("date"),
  };

  const event = {
    load_certified: "load-certified",
  };

  const onInit = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const initialBsQuery = urlParams.get("bs-query");
    if (initialBsQuery) {
      _elements.the_bullshit.innerText = initialBsQuery;
    }

    const bsVerdict = urlParams.get("bs-verdict")
    if (bsVerdict && bsVerdict === "bs-certify"){
      _elements.certified_bs_stamp.style.display = "block"
    } else if (bsVerdict && bsVerdict === "bs-exonerate"){
      _elements.true_fact_stamp.style.display = "block"
    }

    _elements.date.innerText = new Date().toDateString(options={ weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    bsTrack(event.view, initialBsQuery);
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

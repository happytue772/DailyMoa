/* =========================================================
   DailyMoa Live Clock
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const timeElement =
            document.getElementById(
                "liveClockTime"
            );

        const dateElement =
            document.getElementById(
                "liveClockDate"
            );


        // 로그인 전 화면에는 Clock이 없으므로 종료
        if (
            !timeElement ||
            !dateElement
        ) {
            return;
        }


        function updateClock() {

            const now =
                new Date();


            /* -----------------------------
               시간
               ----------------------------- */

            const hours =
                String(
                    now.getHours()
                ).padStart(
                    2,
                    "0"
                );


            const minutes =
                String(
                    now.getMinutes()
                ).padStart(
                    2,
                    "0"
                );


            const seconds =
                String(
                    now.getSeconds()
                ).padStart(
                    2,
                    "0"
                );


            timeElement.textContent =
                `${hours}:${minutes}:${seconds}`;


            /* -----------------------------
               날짜
               ----------------------------- */

            const dateText =
                new Intl.DateTimeFormat(
                    "ko-KR",
                    {
                        month: "2-digit",
                        day: "2-digit",
                        weekday: "short"
                    }
                ).format(
                    now
                );


            dateElement.textContent =
                dateText;

        }


        // 접속하자마자 바로 표시
        updateClock();


        // 이후 1초마다 갱신
        setInterval(
            updateClock,
            1000
        );

    }
);
/* =========================================================
   DailyMoa Dark Mode
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const toggle =
            document.getElementById(
                "themeToggle"
            );

        const icon =
            document.getElementById(
                "themeIcon"
            );


        if (!toggle || !icon) {
            return;
        }


        /* 저장된 테마 확인 */

        const savedTheme =
            localStorage.getItem(
                "dailymoa-theme"
            );


        /* 저장된 다크모드가 있으면 적용 */

        if (savedTheme === "dark") {

            document.documentElement
                .setAttribute(
                    "data-theme",
                    "dark"
                );

        }


        function updateIcon() {

            const currentTheme =
                document.documentElement
                    .getAttribute(
                        "data-theme"
                    );


            if (currentTheme === "dark") {

                icon.textContent = "☀";

                toggle.title =
                    "라이트모드로 전환";

            }

            else {

                icon.textContent = "☾";

                toggle.title =
                    "다크모드로 전환";

            }

        }


        updateIcon();


        /* 클릭 */

        toggle.addEventListener(
            "click",
            function () {

                const currentTheme =
                    document.documentElement
                        .getAttribute(
                            "data-theme"
                        );


                if (currentTheme === "dark") {

                    /* Light */

                    document.documentElement
                        .removeAttribute(
                            "data-theme"
                        );


                    localStorage.setItem(
                        "dailymoa-theme",
                        "light"
                    );

                }

                else {

                    /* Dark */

                    document.documentElement
                        .setAttribute(
                            "data-theme",
                            "dark"
                        );


                    localStorage.setItem(
                        "dailymoa-theme",
                        "dark"
                    );

                }


                updateIcon();

            }
        );

    }
);
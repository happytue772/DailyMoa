document.addEventListener(
    "DOMContentLoaded",
    function () {

        const modal =
            document.getElementById(
                "dailyQuestionModal"
            );

        const launcher =
            document.getElementById(
                "dailyQuestionLauncher"
            );

        const answer =
            document.getElementById(
                "dashboardQuestionAnswer"
            );

        const continueButton =
            document.getElementById(
                "continueQuestionToDiary"
            );


        console.log(
            "Daily Question JS loaded"
        );

        console.log(
            "modal:",
            modal
        );

        console.log(
            "launcher:",
            launcher
        );


        if (
            !modal
            || !launcher
        ) {

            console.error(
                "오늘의 질문 Modal 요소를 찾지 못했습니다."
            );

            return;
        }


        const storageKey =
            modal.dataset.storageKey;

        const diaryUrl =
            modal.dataset.diaryUrl;

        const autoOpen =
            modal.dataset.autoOpen
            === "true";


        // ================================
        // 팝업 열기
        // ================================

        function openQuestionModal() {

            modal.classList.add(
                "show"
            );

            modal.setAttribute(
                "aria-hidden",
                "false"
            );

           console.log(
    "Daily Question JS loaded"
);


document.addEventListener(
    "DOMContentLoaded",
    function () {

        const modal =
            document.getElementById(
                "dailyQuestionModal"
            );

        const launcher =
            document.getElementById(
                "dailyQuestionLauncher"
            );

        const launcherLabel =
            document.getElementById(
                "dailyQuestionLauncherLabel"
            );

        const answer =
            document.getElementById(
                "dashboardQuestionAnswer"
            );

        const continueButton =
            document.getElementById(
                "continueQuestionToDiary"
            );


        console.log(
            "modal:",
            modal
        );

        console.log(
            "launcher:",
            launcher
        );


        if (
            !modal
            || !launcher
        ) {

            console.error(
                "오늘의 질문 Modal 요소를 찾지 못했습니다."
            );

            return;
        }


        const storageKey =
            modal.dataset.storageKey;

        const diaryUrl =
            modal.dataset.diaryUrl;

        const autoOpen =
            modal.dataset.autoOpen
            === "true";


        console.log(
            "autoOpen:",
            autoOpen
        );


        /* =================================================
           기존 답변 복원
           ================================================= */

        if (
            answer
            && storageKey
        ) {

            const savedAnswer =
                sessionStorage.getItem(
                    storageKey
                );


            if (savedAnswer) {

                answer.value =
                    savedAnswer;


                if (launcherLabel) {

                    launcherLabel.textContent =
                        "답변 계속하기";

                }

            }

        }


        /* =================================================
           Modal 열기
           ================================================= */

        function openQuestionModal() {

            modal.classList.add(
                "show"
            );


            modal.setAttribute(
                "aria-hidden",
                "false"
            );


            /*
             * 중요:
             * body에 overflow:hidden을 주지 않는다.
             *
             * 그래서 Modal이 떠 있어도
             * Dashboard Scroll이 가능하다.
             */


            if (answer) {

                setTimeout(
                    function () {

                        answer.focus();

                    },
                    150
                );

            }

        }


        /* =================================================
           Modal 닫기
           ================================================= */

        function closeQuestionModal() {

            modal.classList.remove(
                "show"
            );


            modal.setAttribute(
                "aria-hidden",
                "true"
            );

        }


        /* =================================================
           Launcher
           ================================================= */

        launcher.addEventListener(
            "click",
            function () {

                openQuestionModal();

            }
        );


        /* =================================================
           닫기 버튼
           ================================================= */

        document
            .querySelectorAll(
                "[data-question-close]"
            )
            .forEach(
                function (button) {

                    button.addEventListener(
                        "click",
                        function () {

                            closeQuestionModal();

                        }
                    );

                }
            );


        /* =================================================
           ESC
           ================================================= */

        document.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key
                    === "Escape"
                    &&
                    modal.classList
                        .contains("show")
                ) {

                    closeQuestionModal();

                }

            }
        );


        /* =================================================
           답변 임시 저장
           ================================================= */

        if (
            answer
            && storageKey
        ) {

            answer.addEventListener(
                "input",
                function () {

                    sessionStorage.setItem(
                        storageKey,
                        answer.value
                    );


                    if (
                        launcherLabel
                        && answer.value.trim()
                    ) {

                        launcherLabel.textContent =
                            "답변 계속하기";

                    }

                    else if (
                        launcherLabel
                    ) {

                        launcherLabel.textContent =
                            "오늘의 질문";

                    }

                }
            );

        }


        /* =================================================
           Diary로 이동
           ================================================= */

        if (
            continueButton
            && diaryUrl
        ) {

            continueButton.addEventListener(
                "click",
                function () {

                    if (
                        answer
                        && storageKey
                    ) {

                        sessionStorage.setItem(
                            storageKey,
                            answer.value
                        );

                    }


                    window.location.href =
                        diaryUrl
                        + "?from_dashboard=1";

                }
            );

        }


        /* =================================================
           로그인 직후 자동 표시
           ================================================= */

        if (autoOpen) {

            setTimeout(
                function () {

                    openQuestionModal();

                },
                400
            );

        }

    }
);

        }


        // ================================
        // 팝업 닫기
        // ================================

        function closeQuestionModal() {

            modal.classList.remove(
                "show"
            );

            modal.setAttribute(
                "aria-hidden",
                "true"
            );

            document.body.classList.remove(
                "question-modal-open"
            );

        }


        // ================================
        // 우측 하단 버튼
        // ================================

        launcher.addEventListener(
            "click",
            function () {

                console.log(
                    "오늘의 질문 버튼 클릭"
                );

                openQuestionModal();

            }
        );


        // ================================
        // 닫기 버튼
        // ================================

        document
            .querySelectorAll(
                "[data-question-close]"
            )
            .forEach(
                function (button) {

                    button.addEventListener(
                        "click",
                        closeQuestionModal
                    );

                }
            );


        // ================================
        // ESC로 닫기
        // ================================

        document.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Escape"
                ) {

                    closeQuestionModal();

                }

            }
        );


        // ================================
        // 기존 답변 복원
        // ================================

        if (
            answer
            && storageKey
        ) {

            const savedAnswer =
                sessionStorage.getItem(
                    storageKey
                );


            if (savedAnswer) {

                answer.value =
                    savedAnswer;

            }


            answer.addEventListener(
                "input",
                function () {

                    sessionStorage.setItem(
                        storageKey,
                        answer.value
                    );

                }
            );

        }


        // ================================
        // Diary로 이동
        // ================================

        if (
            continueButton
            && diaryUrl
        ) {

            continueButton.addEventListener(
                "click",
                function () {

                    if (
                        answer
                        && storageKey
                    ) {

                        sessionStorage.setItem(
                            storageKey,
                            answer.value
                        );

                    }


                    window.location.href =
                        diaryUrl
                        + "?from_dashboard=1";

                }
            );

        }


        // ================================
        // 로그인 직후 자동 팝업
        // ================================

        if (autoOpen) {

            setTimeout(
                function () {

                    openQuestionModal();

                },
                400
            );

        }

    }
);
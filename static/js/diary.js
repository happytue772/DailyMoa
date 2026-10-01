document.addEventListener(
    "DOMContentLoaded",
    function () {

        const button =
            document.getElementById(
                "useDailyQuestion"
            );

        const card =
            document.getElementById(
                "dailyQuestionCard"
            );

        const textarea =
            document.getElementById(
                "diaryContent"
            );


        if (
            !card
            || !textarea
        ) {
            return;
        }


        const question =
            card.dataset.question
            || "";

        const storageKey =
            card.dataset.storageKey;


        const params =
            new URLSearchParams(
                window.location.search
            );


        const fromDashboard =
            params.get(
                "from_dashboard"
            )
            === "1";


        /* =================================================
           Dashboard 답변 가져오기
           ================================================= */

        if (
            fromDashboard
            && storageKey
        ) {

            const savedAnswer =
                sessionStorage.getItem(
                    storageKey
                );


            if (
                savedAnswer
                && !textarea.value.trim()
            ) {

                textarea.value =
                    question
                    + "\n\n"
                    + savedAnswer;

            }

        }


        /* =================================================
           질문으로 시작하기
           ================================================= */

        if (button) {

            button.addEventListener(
                "click",
                function () {

                    if (
                        textarea.value.trim()
                        === ""
                    ) {

                        textarea.value =
                            question
                            + "\n\n";

                    }

                    else {

                        textarea.value =
                            question
                            + "\n\n"
                            + textarea.value;

                    }


                    textarea.focus();

                }
            );

        }


        /* =================================================
           Diary 저장 후 임시 답변 제거
           ================================================= */

        const form =
            textarea.closest(
                "form"
            );


        if (
            form
            && storageKey
        ) {

            form.addEventListener(
                "submit",
                function () {

                    sessionStorage.removeItem(
                        storageKey
                    );

                }
            );

        }

    }
);
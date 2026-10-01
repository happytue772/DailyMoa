let calendar;

let editingScheduleId = null;


document.addEventListener(
    "DOMContentLoaded",
    function () {

        const calendarEl =
            document.getElementById(
                "calendar"
            );


        if (!calendarEl) {
            return;
        }


        calendar =
            new FullCalendar.Calendar(
                calendarEl,
                {

                    initialView:
                        "dayGridMonth",

                    locale:
                        "ko",

                    height:
                        "auto",


                    /* 일정 + Diary 감정 */

                    eventSources: [

                        {
                            url:
                                "/api/schedules"
                        },

                        {
                            url:
                                "/diary/api/moods"
                        }

                    ],


                    eventClick:
                        function (info) {

                            const type =
                                info.event
                                    .extendedProps
                                    .type;


                            /* Diary 감정 */

                            if (
                                type === "diary"
                            ) {

                                window.location.href =
                                    info.event
                                        .extendedProps
                                        .detailUrl;

                                return;
                            }


                            /* 일반 일정 */

                            openScheduleDetail(
                                info.event
                            );

                        }

                }
            );


        calendar.render();

    }
);


/* =========================================================
   일정 추가
   ========================================================= */

function openScheduleForm() {

    editingScheduleId = null;


    document.getElementById(
        "scheduleModalTitle"
    ).textContent =
        "일정 등록";


    document.getElementById(
        "scheduleTitle"
    ).value = "";


    document.getElementById(
        "scheduleStart"
    ).value = "";


    document.getElementById(
        "scheduleEnd"
    ).value = "";


    document.getElementById(
        "scheduleContent"
    ).value = "";


    document
        .getElementById(
            "scheduleDeleteButton"
        )
        .classList
        .add("hidden");


    document
        .getElementById(
            "scheduleModal"
        )
        .classList
        .remove("hidden");

}


/* =========================================================
   일정 상세 / 수정
   ========================================================= */

function openScheduleDetail(event) {

    editingScheduleId =
        event.id;


    document.getElementById(
        "scheduleModalTitle"
    ).textContent =
        "일정 상세 / 수정";


    document.getElementById(
        "scheduleTitle"
    ).value =
        event.title;


    document.getElementById(
        "scheduleStart"
    ).value =
        toDateTimeInput(
            event.start
        );


    document.getElementById(
        "scheduleEnd"
    ).value =
        event.end
            ? toDateTimeInput(
                event.end
            )
            : "";


    document.getElementById(
        "scheduleContent"
    ).value =
        event.extendedProps.content
        || "";


    document
        .getElementById(
            "scheduleDeleteButton"
        )
        .classList
        .remove("hidden");


    document
        .getElementById(
            "scheduleModal"
        )
        .classList
        .remove("hidden");

}


function closeScheduleForm() {

    editingScheduleId = null;


    document
        .getElementById(
            "scheduleModal"
        )
        .classList
        .add("hidden");

}


/* =========================================================
   저장
   ========================================================= */

async function saveSchedule() {

    const title =
        document.getElementById(
            "scheduleTitle"
        ).value.trim();


    const start =
        document.getElementById(
            "scheduleStart"
        ).value;


    const end =
        document.getElementById(
            "scheduleEnd"
        ).value;


    const content =
        document.getElementById(
            "scheduleContent"
        ).value.trim();


    if (!title || !start) {

        alert(
            "제목과 시작 시간을 입력해주세요."
        );

        return;
    }


    const url =
        editingScheduleId
            ? `/api/schedules/${editingScheduleId}`
            : "/api/schedules";


    const method =
        editingScheduleId
            ? "PUT"
            : "POST";


    const response =
        await fetch(
            url,
            {

                method,

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(
                        {
                            title,
                            start,
                            end,
                            content
                        }
                    )

            }
        );


    if (!response.ok) {

        alert(
            "일정 저장 중 오류가 발생했습니다."
        );

        return;
    }


    calendar.refetchEvents();

    closeScheduleForm();

}


/* =========================================================
   삭제
   ========================================================= */

async function deleteCurrentSchedule() {

    if (!editingScheduleId) {
        return;
    }


    const confirmed =
        confirm(
            "이 일정을 삭제하시겠습니까?"
        );


    if (!confirmed) {
        return;
    }


    const response =
        await fetch(
            `/api/schedules/${editingScheduleId}`,
            {
                method:
                    "DELETE"
            }
        );


    if (response.ok) {

        calendar.refetchEvents();

        closeScheduleForm();

    }

}


/* =========================================================
   datetime-local 변환
   ========================================================= */

function toDateTimeInput(date) {

    const timezoneOffset =
        date.getTimezoneOffset()
        * 60000;


    return new Date(
        date.getTime()
        - timezoneOffset
    )
        .toISOString()
        .slice(0, 16);

}
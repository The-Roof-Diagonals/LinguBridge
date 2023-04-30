import './AppointmentDate.css'

function AppointmentDate(props: any) {
    const date = new Date(props.date);
    const month = date.toLocaleString('en-US', { month: 'long' });
    const day = date.toLocaleString('en-US', { day: '2-digit' });
    const year = date.getFullYear();
    const hour = date.getHours();
    const min = date.getMinutes();
    let minutes;
    if (min < 10)
        minutes = "0" + min;
    else
        minutes = min;

    return (
        <div className="appointment-date">
            <div className="appointment-date__month">{day + " " + month}</div>
            <div className="appointment-date__day">{hour + ":" + minutes}</div>
            <div className="appointment-date__year">{year}</div>
        </div>
    );

}

export default AppointmentDate;
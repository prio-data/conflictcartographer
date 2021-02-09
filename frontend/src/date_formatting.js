
const months=[
   "January",
   "February",
   "March",
   "April",
   "May",
   "June",
   "July",
   "August",
   "September",
   "October",
   "November",
   "December",
]

export function format_date(date){
   if(typeof(date)==="string"){
      date = new Date(date)
   }
   return `${months[date.getMonth()]} ${date.getFullYear()}`
}

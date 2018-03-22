val months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

fun is_older (prx: int*int*int, pry: int*int*int) =
	if #1 prx < #1 pry
		then true
	else if #1 prx = #1 pry andalso #2 prx < #2 pry
		then true
	else if #1 prx = #1 pry andalso #2 prx = #2 pry andalso #3 prx < #3 pry
		then true
	else false

fun number_in_month (xs: (int*int*int) list, month: int)=
	if null xs
	then 0
	else if #2 (hd xs) = month
	then number_in_month(tl xs, month) + 1
	else number_in_month(tl xs, month)

fun number_in_months (xs: (int*int*int) list, ys: int list) =
	if null ys
	then 0
	else
		number_in_month(xs, hd ys) + number_in_months(xs, tl ys)

fun dates_in_month (xs: (int*int*int) list, y: int) =
	if null xs
	then []
	else if #2 (hd xs) = y
	then
		hd xs::dates_in_month (tl xs, y)
	else
		dates_in_month (tl xs, y)

fun dates_in_months (xs: (int*int*int) list, ys: int list)=
	if null ys
	then []
	else dates_in_month (xs, hd ys) @ dates_in_months (xs, tl ys)

fun get_nth (xs: string list, y: int) =
	if y = 1
	then hd xs
	else get_nth (tl xs, y-1)

fun date_to_string (x: int*int*int) =
	get_nth (months, #2 x) ^ " " ^ Int.toString (#3 x) ^ ", " ^ Int.toString (#1 x)

fun get_nth_int (xs: int list, n: int) =
(*helper function to get nth n elements of list*)
if n = 1
then hd xs
else get_nth_int (tl xs, n-1)

fun number_before_reaching_sum (x: int, xs: int list) =
	if hd xs >= x
	then 0
	else if hd xs < x andalso hd xs + hd (tl xs) >= x
	then 1
	else number_before_reaching_sum (x - hd xs , tl xs) + 1

fun what_month (x: int) =
	let
		val month_day_list  = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	in
		number_before_reaching_sum (x, month_day_list) + 1
	end

fun month_range (day1: int, day2: int) =
	if day1 > day2
	then []
	else
		what_month (day1) :: month_range (day1 + 1, day2)

fun oldest (xs: (int*int*int) list) =
	if null xs 
	then NONE
	else if null (tl xs) orelse (null (tl (tl xs)) andalso is_older (hd xs, hd (tl xs)))
	then SOME (hd xs)
	else if null (tl (tl xs)) andalso is_older (hd xs, hd (tl xs)) = false
	then SOME (hd (tl xs))
	else if is_older (hd xs, hd (tl xs))
	then oldest (hd xs :: tl (tl xs))
	else oldest (tl xs)

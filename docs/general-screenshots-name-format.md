# Screenshots Name Format

Since v0.1.60, it’s now possible to change format of screenshot names. Here are supported replacements:

- `{CarID}`: car ID (aka folder name);
- `{SkinID}`: skin ID;
- `{TrackID}`: track ID;
- `{LayoutID}`: layout ID;
- `{Car}`: car name;
- `{Track}`: track name;
- `{PPFilter}`: PP filter name, or “unknown” if it’s disabled;
- `{Year}`: year, like 2020;
- `{Month}`: month with two digits (01…12);
- `{Day}`: day with two digits (01…31);
- `{Hour}`: hours with two digits (00…23);
- `{Min}`: minutes with two digits (00…59);
- `{Sec}`: seconds with two digits (00…59);
- `{YearRaw}`: year in Kunos format (subtracting 1900, so 120 instead of 2020)
- `{MonthNum}`: month in Kunos format (0…11)
- `{DayNum}`: day (1…31);
- `{HourNum}`: hours (0…23);
- `{MinNum}`: minutes (0…59);
- `{SecNum}`: seconds (0…59).

Examples:

- `Screenshot_{CarID}_{TrackID}_{DayNum}-{MonthNum}-{YearRaw}-{HourNum}-{MinNum}-{SecNum}`

  Kunos format, results in something like “Screenshot_ks_toyota_gt86_ks_brands_hatch_4-5-120-19-46-32”.

- `{Year}{Month}{Day}-{Hour}{Min}{Sec}-{Track}-{Car}`

  Gives nice ordering by date, results in something like “20200505-194632-Brands Hatch-Toyota GT86”.

- `{Year}-{Month}/{Year}{Month}{Day}-{Hour}{Min}{Sec}-{TrackID}-{CarID}`

  Groups screenshots by month, results in something like “2020-05\20200505-194632-ks_brands_hatch-ks_toyota_gt86”.

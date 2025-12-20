
function pluralizeRecords(n) {
  let word;

  let lastTwo = n % 100;
  let last = n % 10;

  if (lastTwo >= 11 && lastTwo <= 14) {
    word = "записей";
  } else if (last === 1) {
    word = "запись";
  } else if (last >= 2 && last <= 4) {
    word = "записи";
  } else {
    word = "записей";
  }

  return "В результате выполнения запроса было найдено " + n + " " + word;
}

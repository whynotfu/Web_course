function getSortedArray(array, key) {

  let result = [];
  for (let i = 0; i < array.length; i++) {
    result[i] = array[i];
  }


  for (let i = 0; i < result.length - 1; i++) {
    for (let j = 0; j < result.length - 1 - i; j++) {
      if (result[j][key] > result[j + 1][key]) {
        let temp = result[j];
        result[j] = result[j + 1];
        result[j + 1] = temp;
      }
    }
  }

  return result;
}
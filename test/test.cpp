#include <iostream>
using namespace std;

int main() {

  //declares num as a floating point number variable
  float num;

  // Displays this text to the console
  cout << "Give me a number:" << endl;

  // Takes the user's input and stores it in num
  cin >> num;

  // Displays to the console
  float halved;
  halved = num/2.0;
  cout << "This is your number halved: " << halved << endl;
  system ("pause");
  return 0;
}

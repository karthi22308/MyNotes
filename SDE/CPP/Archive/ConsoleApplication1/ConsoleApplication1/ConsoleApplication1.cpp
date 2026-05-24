#include <iostream>
#include<string.h>
#include <algorithm>
#include <limits.h>
#include <sstream>
#include <fstream>
using namespace std;
class test {
public:
    int ka;
    int dl;

    test(int k, int s) {
        ka = k;
        //cout<<"hi"<<t
        dl = s;
    }
};

int main()
{
    char a = 'r';
    int k = (int)a;
    cout << k << endl;
    string s = to_string(k);
    cout << s << endl;
    string str = "karthick";
    sort(str.begin(), str.end());
    cout << str << endl;
    string w = "100";
    int wq = stoi(w);
    cout << wq << endl;
    string no = "12 56 76 56 43 09";

    stringstream x(no);
    while (x) {
        int n;
        x >> n;
        cout << n;
    }

    cout << endl;
    ofstream outputFile("output.txt");
    if (outputFile.is_open()) {
        outputFile << "hello file";
    }

    test obj(1, 4);
    cout << obj.ka << endl;
    cout << obj.dl << endl;


    return 0;
}
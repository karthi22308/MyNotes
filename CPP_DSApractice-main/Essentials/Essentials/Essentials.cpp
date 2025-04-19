#include <iostream>
#include <vector>
#include <stack>
#include <unordered_map>
using namespace std;

int main()
{
	vector<string> sentances = { "test one test application","test two","test three" };
	vector<string> output;


	for (string s : sentances) {
		string word ="";
		for (char c : s) {
			word += c;
			if (c == ' ') {
				word = "";
			}

		}
		output.push_back(word);
	}
	for (string s : output) {
		cout << s << " ";
	}

	
	
}



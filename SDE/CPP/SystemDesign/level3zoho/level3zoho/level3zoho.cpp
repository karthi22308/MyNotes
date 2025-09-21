// level3zoho.cpp : Complete employee management system for Zoho-like hierarchy

#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include <unordered_map>
using namespace std;

class employee {
public:
    int id;
    string name;
    int age;
    string department;
    string designation;
    int managerid;

    employee(int id, string name, int age, string dept, string design, int managerid) {
        this->id = id;
        this->name = name;
        this->age = age;
        this->department = dept;
        this->designation = design;
        this->managerid = managerid;
    }
};

class database {
private:
    vector<employee> employeelist;

public:
    database() {
        // preload
        employeelist.push_back(employee(1, "sriram", 45, "Management", "CEO", 0));
        employeelist.push_back(employee(2, "mukund", 43, "HR", "hr manager", 1));
        employeelist.push_back(employee(3, "sebastian", 38, "Finance", "finance manager", 1));
        employeelist.push_back(employee(4, "aashritha", 32, "product management", "dev manager", 1));
        employeelist.push_back(employee(5, "mohammadrafi", 35, "HR", "hr lead", 2));
        employeelist.push_back(employee(6, "anjalikumar", 29, "HR", "hr associate", 5));
        employeelist.push_back(employee(7, "joseph", 40, "Finance", "finance associate", 3));
        employeelist.push_back(employee(8, "ramachandran", 27, "product development", "Tech lead", 4));
        employeelist.push_back(employee(9, "abhinayashankar", 23, "product development", "system developer", 8));
        employeelist.push_back(employee(10, "imrankhan", 28, "product testing", "qa lead", 8));
    }

    int findemployeebyname(string name) {
        for (employee& obj : employeelist) {
            if (obj.name == name) return obj.id;
        }
        return 0;
    }

    employee findemployee(int id) {
        for (employee& obj : employeelist) {
            if (obj.id == id) return obj;
        }
        return employee(0, " ", 0, "", "", 0);
    }

    bool ismanager(int id) {
        for (employee& obj : employeelist) {
            if (obj.managerid == id) return true;
        }
        return false;
    }

    void printall() {
        cout << "Employee List:" << endl;
        for (employee& e : employeelist) {
            cout << "ID:" << e.id << " name:" << e.name << " age:" << e.age
                << " department:" << e.department << " designation:" << e.designation
                << " Reporting to:" << findemployee(e.managerid).name << endl;
        }
    }

    void Removeemployee() {
        cout << "\nEnter employee id to be deleted: ";
        int n; cin >> n;
        if (n == 1) {
            cout << "CEO cannot be deleted!\n"; return;
        }
        if (ismanager(n)) {
            cout << "\nEmployee is a manager. Enter replacement manager id (or 0 to assign to their manager): ";
            int r; cin >> r;
            if (r == 0) r = findemployee(n).managerid;
            for (employee& ob : employeelist) {
                if (ob.managerid == n) ob.managerid = r;
            }
        }
        for (auto it = employeelist.begin(); it != employeelist.end(); ++it) {
            if (it->id == n) {
                cout << "Deleting employee " << it->name << endl;
                employeelist.erase(it);
                break;
            }
        }
    }

    void printreportees() {
        string name; cout << "Enter employee name: "; cin >> name;
        int n = findemployeebyname(name);
        if (ismanager(n)) {
            for (employee& e : employeelist) {
                if (e.managerid == n) {
                    cout << "ID:" << e.id << " name:" << e.name << " age:" << e.age
                        << " department:" << e.department << " designation:" << e.designation
                        << " Reporting to:" << findemployee(e.managerid).name << endl;
                }
            }
        }
        else cout << "No reportees found.\n";
    }

    void printtree() {
        string name; cout << "Enter employee name: "; cin >> name;
        int n = findemployeebyname(name);
        if (n != 0) {
            int k = n;
            while (k != 0) {
                employee obj = findemployee(k);
                cout << obj.name;
                if (obj.managerid != 0) cout << " -> ";
                k = obj.managerid;
            }
            cout << endl;
        }
        else cout << "Invalid employee name\n";
    }

    void summary() {
        unordered_map<string, int> department, designation, manager;
        for (employee& e : employeelist) {
            department[e.department]++;
            designation[e.designation]++;
            if (ismanager(e.id)) {
                int count = 0;
                for (employee& t : employeelist) if (t.managerid == e.id) count++;
                manager[e.name] = count;
            }
        }
        cout << "\nDepartment summary:\n";
        for (auto& it : department) cout << it.first << ": " << it.second << endl;
        cout << "\nDesignation summary:\n";
        for (auto& it : designation) cout << it.first << ": " << it.second << endl;
        cout << "\nManager summary (#reportees):\n";
        for (auto& it : manager) cout << it.first << ": " << it.second << endl;
    }

    // 🔹 Find with criteria
    vector<employee> findall(vector<employee> list, int column, string value, string criteria) {
        vector<employee> outlist;
        for (employee& e : list) {
            string field;
            if (column == 1) field = e.name;
            else if (column == 3) field = e.department;
            else if (column == 4) field = e.designation;
            else if (column == 5) field = findemployee(e.managerid).name;

            if (criteria == "equals" && field == value) outlist.push_back(e);
            else if (criteria == "notequals" && field != value) outlist.push_back(e);
            else if (criteria == "startswith" && field.rfind(value, 0) == 0) outlist.push_back(e);
            else if (criteria == "endswith" && field.size() >= value.size() &&
                field.compare(field.size() - value.size(), value.size(), value) == 0) outlist.push_back(e);
            else if (criteria == "contains" && field.find(value) != string::npos) outlist.push_back(e);
            else if (criteria == "notcontains" && field.find(value) == string::npos) outlist.push_back(e);
        }
        return outlist;
    }

    void searchandupdate() {
        vector<employee> temp = employeelist;
        while (true) {
            cout << "\nSearch and Update Menu\n1.Name\n2.Age\n3.Department\n4.Designation\n5.Reporting to\n6.Quit\nChoice: ";
            int n; cin >> n;
            if (n == 6) return;

            string s; cout << "Enter value: "; cin >> s;
            cout << "\nFilter criteria:\n1.Equals\n2.Not equals\n3.Starts with\n4.Ends with\n5.Contains\n6.Not contains\n7.Quit\nChoice: ";
            int j; cin >> j;
            if (j == 7) return;

            string crit;
            if (j == 1) crit = "equals";
            else if (j == 2) crit = "notequals";
            else if (j == 3) crit = "startswith";
            else if (j == 4) crit = "endswith";
            else if (j == 5) crit = "contains";
            else if (j == 6) crit = "notcontains";

            temp = findall(temp, n, s, crit);

            cout << "\nAvailable employees:\n";
            for (employee& e : temp) {
                cout << "ID:" << e.id << " name:" << e.name << " age:" << e.age
                    << " department:" << e.department << " designation:" << e.designation
                    << " Reporting to:" << findemployee(e.managerid).name << endl;
            }

            cout << "\nOptions:\n1.Add another criteria\n2.Update record(s)\n3.Exit\nChoice: ";
            int opt; cin >> opt;
            if (opt == 3) return;
            else if (opt == 2) {
                cout << "Select column to update:\n1.Name\n2.Age\n3.Department\n4.Designation\n5.Reporting to\nChoice: ";
                int coll; cin >> coll;
                cout << "Enter new value: ";
                string alt; cin >> alt;

                for (employee& e : employeelist) {
                    for (employee& f : temp) {
                        if (e.id == f.id) {
                            if (coll == 1) e.name = alt;
                            else if (coll == 2) e.age = stoi(alt);
                            else if (coll == 3) e.department = alt;
                            else if (coll == 4) e.designation = alt;
                            else if (coll == 5) e.managerid = findemployeebyname(alt);
                        }
                    }
                }
                cout << "Update successful!\n";
            }
        }
    }

    void menu() {
        while (true) {
            int n;
            cout << "\nMain Menu\n1.Show all records\n2.Search and update\n3.Remove employee\n4.Manager report\n5.Reporting tree\n6.Summary report\n7.Exit\nChoice: ";
            cin >> n;
            switch (n) {
            case 1: printall(); break;
            case 2: searchandupdate(); break;
            case 3: Removeemployee(); break;
            case 4: printreportees(); break;
            case 5: printtree(); break;
            case 6: summary(); break;
            case 7: return;
            default: cout << "Invalid choice\n";
            }
        }
    }
};

int main() {
    database obj;
    obj.menu();
    return 0;
}

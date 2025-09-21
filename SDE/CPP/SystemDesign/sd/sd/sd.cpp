#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
using namespace std;

class SeatType {
private:
    string type;
    int capacity;
    int waitingCapacity;
    vector<string> booked;
    vector<string> waiting;

public:
    SeatType(string t, int cap = 60, int waitCap = 10) {
        type = t;
        capacity = cap;
        waitingCapacity = waitCap;
    }

    // Booking
    void bookTicket(const string& name) {
        if ((int)booked.size() < capacity) {
            booked.push_back(name);
            cout << "✅ Ticket confirmed for " << name << " in " << type << endl;
        }
        else if ((int)waiting.size() < waitingCapacity) {
            waiting.push_back(name);
            cout << "⚠️ No seats available in " << type << ". "
                << name << " added to waiting list.\n";
        }
        else {
            cout << "❌ Sorry! No seats or waiting available in " << type << endl;
        }
    }

    // Availability
    void checkAvailability() {
        cout << type << " -> Seats left: " << capacity - booked.size()
            << ", Waiting left: " << waitingCapacity - waiting.size() << endl;
    }

    // Cancellation
    void cancelTicket(const string& name) {
        auto it = find(booked.begin(), booked.end(), name);
        if (it != booked.end()) {
            booked.erase(it);
            cout << "❌ Booking cancelled for " << name << " in " << type << endl;
            if (!waiting.empty()) {
                string next = waiting.front();
                waiting.erase(waiting.begin());
                booked.push_back(next);
                cout << "✅ " << next << " moved from waiting to confirmed in " << type << endl;
            }
            return;
        }
        auto it2 = find(waiting.begin(), waiting.end(), name);
        if (it2 != waiting.end()) {
            waiting.erase(it2);
            cout << "❌ Removed " << name << " from waiting list of " << type << endl;
            return;
        }
        cout << "⚠️ No booking found for " << name << " in " << type << endl;
    }

    // Chart preparation
    void prepareChart() {
        cout << "\n==== " << type << " ====\n";
        cout << "Confirmed (" << booked.size() << "): ";
        for (auto& n : booked) cout << n << " ";
        cout << "\nWaiting (" << waiting.size() << "): ";
        for (auto& n : waiting) cout << n << " ";
        cout << "\n";
    }
};

class RailwayReservation {
private:
    SeatType ac{ "AC Coach" };
    SeatType nonAc{ "Non-AC Coach" };
    SeatType seater{ "Seater" };

public:
    void menu() {
        int choice;
        string name;
        while (true) {
            cout << "\n====== Railway Reservation System ======\n";
            cout << "1. Book Ticket\n2. Check Availability\n3. Cancel Ticket\n4. Prepare Chart\n5. Exit\n";
            cout << "Enter choice: ";
            cin >> choice;

            switch (choice) {
            case 1: {
                cout << "Enter passenger name: ";
                cin >> name;
                cout << "Choose Coach (1-AC, 2-NonAC, 3-Seater): ";
                int ch; cin >> ch;
                if (ch == 1) ac.bookTicket(name);
                else if (ch == 2) nonAc.bookTicket(name);
                else if (ch == 3) seater.bookTicket(name);
                else cout << "Invalid coach!\n";
                break;
            }
            case 2: {
                ac.checkAvailability();
                nonAc.checkAvailability();
                seater.checkAvailability();
                break;
            }
            case 3: {
                cout << "Enter passenger name to cancel: ";
                cin >> name;
                cout << "Choose Coach (1-AC, 2-NonAC, 3-Seater): ";
                int ch; cin >> ch;
                if (ch == 1) ac.cancelTicket(name);
                else if (ch == 2) nonAc.cancelTicket(name);
                else if (ch == 3) seater.cancelTicket(name);
                else cout << "Invalid coach!\n";
                break;
            }
            case 4: {
                ac.prepareChart();
                nonAc.prepareChart();
                seater.prepareChart();
                break;
            }
            case 5:
                cout << "👋 Thank you for using Railway Reservation System!\n";
                return;
            default:
                cout << "Invalid choice! Try again.\n";
            }
        }
    }
};

class seat {
private :
   
        int seatmap[8][8];
public:
    seat()
    {
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                seatmap[i][j] = 0;
            }
        }


    }
    bool avlbl(int i, int j, int n) {
        for (int x = i; x <= j; x++) {
            if (seatmap[n][x] == 1) return false;
        }
        return true;
    }
    void book(int i, int j, int n) {
       int booked = 0;
        for (int k = 0; k < 8; k++) {
            if (avlbl(i, j, k) )
            {
                for (int x = i; x < j; x++) {
                    seatmap[k][x] = 1;
                }
                booked++;
            }
            if (booked == n) {
                cout << "booking done";
                return;
            }

        }
    }
    void printlist() {
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                cout << seatmap[i][j];
            }
            cout << "\n";
        }
    }

};

class systems {
public:
    seat ac{};
    seat sl{};
    systems()
    {
        while (true) {
            int k;
            cin >> k;
            switch (k) {
            case 1:
                cout << "ac chart" << endl;
                ac.printlist();
                cout << "sl chart" << endl;
                sl.printlist();
                break;
            case 2:
                cout << "book ac";
                int i, j, n;
                cin >> i >> j >> n;
                ac.book(i, j, n);
                break;
            case 3:
                cout << "book sl";
              //  int a, b, c;
                cin >> i >> j >> n;
                sl.book(i, j, n);
                break;

            }


        }
    }

};

int main() {
   /* RailwayReservation system;
    system.menu();*/
    //vector<string> names;
    //cout << "hello";
    //names.push_back("karthick");
    //names.push_back("karthickwww");
    //names.push_back("kartdddhickwww");


    //auto it = find(names.begin(), names.end(), "karthick");
    //if (it != names.end()) {
    //    names.erase(it);
    //}
    systems sys;



   
    return 0;
}

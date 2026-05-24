import { Component, signal,Signal, computed } from '@angular/core';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-signalscomp',
  imports: [FormsModule],
  templateUrl: './signalscomp.html',
  styleUrl: './signalscomp.css',
})
export class Signalscomp {
count = signal(0);
double : Signal<number> =computed(()=> this.count() * 2);
  add(){
    this.count.set(this.count() +1);

  }
}

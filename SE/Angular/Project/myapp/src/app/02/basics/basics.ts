import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { Counter } from '../../counter/counter';


@Component({
  selector: 'app-basics',
  imports: [RouterOutlet,FormsModule,Counter,Basics],
  templateUrl: './basics.html',
  styleUrl: './basics.css',
})
export class Basics {
  protected readonly title = signal('myapp');
  head = "karthick";
  count=0;
  img="C:\\Users\\karth\\Downloads\\Telegram Desktop\\IMG_20251213_085816";


  getname(){
    return "superstar"
  }
  onclick(){
    this.count++;
  }

}

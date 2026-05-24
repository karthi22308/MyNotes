import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
<<<<<<< HEAD
=======
import { Counter } from '../../counter/counter';
>>>>>>> 8d7958d59e09366ff83656dece91891ffb640986


@Component({
  selector: 'app-basics',
<<<<<<< HEAD
  imports: [RouterOutlet,FormsModule,Basics],
=======
  imports: [RouterOutlet,FormsModule,Counter,Basics],
>>>>>>> 8d7958d59e09366ff83656dece91891ffb640986
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

import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-form',
  imports: [CommonModule,FormsModule],
  templateUrl: './form.html',
  styleUrl: './form.css',
})
export class Form {
  car="";
  onclick(){
console.log(this.car);
this.car="";

  }




}

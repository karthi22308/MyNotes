import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { high } from '../customhigh';

@Component({
  selector: 'app-directivecomp',
  imports: [CommonModule,FormsModule,high],
  templateUrl: './directivecomp.html',
  styleUrl: './directivecomp.css',
})
export class Directivecomp {
  showme=false;

  movies = [
"ram",
"kutty",
"jk",
"test"   
  ]

}

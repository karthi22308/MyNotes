import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-pipescomp',
  imports: [CommonModule],
  templateUrl: './pipescomp.html',
  styleUrl: './pipescomp.css',
})
export class Pipescomp {
  date = new Date();
  word="hello world";
  movies =["ko","ngk","pipe","ra"];


}

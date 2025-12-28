import { Component } from '@angular/core';
import { Basics } from './02/basics/basics';
import { Signalscomp } from './03/signalscomp/signalscomp';
import { Directivecomp } from './04/directivecomp/directivecomp';
import { Pipescomp } from './05/pipescomp/pipescomp';


@Component({
  selector: 'app-root',
  imports: [Basics,Signalscomp,Directivecomp,Pipescomp],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
 
}
 
import { Component } from '@angular/core';
import { Basics } from './02/basics/basics';
import { Signalscomp } from './03/signalscomp/signalscomp';
import { Directivecomp } from './04/directivecomp/directivecomp';
import { Pipescomp } from './05/pipescomp/pipescomp';
import { testapp } from './06/app/app';


@Component({
  selector: 'app-root',
  imports: [Basics,Signalscomp,Directivecomp,Pipescomp,testapp],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
 
}
 
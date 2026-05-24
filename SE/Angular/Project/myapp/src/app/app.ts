import { Component } from '@angular/core';
import { Basics } from './02/basics/basics';
import { Signalscomp } from './03/signalscomp/signalscomp';
import { Directivecomp } from './04/directivecomp/directivecomp';
import { Pipescomp } from './05/pipescomp/pipescomp';
<<<<<<< HEAD
import { testapp } from './06/app/app';
=======
>>>>>>> 8d7958d59e09366ff83656dece91891ffb640986


@Component({
  selector: 'app-root',
<<<<<<< HEAD
  imports: [Basics,Signalscomp,Directivecomp,Pipescomp,testapp],
=======
  imports: [Basics,Signalscomp,Directivecomp,Pipescomp],
>>>>>>> 8d7958d59e09366ff83656dece91891ffb640986
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
 
}
 
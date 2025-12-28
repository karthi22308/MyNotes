import { Directive, ElementRef, HostListener, Input } from '@angular/core';



// this is a custom directive
@Directive({
  selector: '[high]',
})
export class high {
  @Input() custom = ""

  constructor(private el : ElementRef) { }

  @HostListener('mouseenter') onMouseEnter(){
this.highlight(this.custom || "yellow");
  }
    @HostListener('mouseleave') onMouseLeave(){
    this.highlight('');
  }

  private highlight(color: any){
    this.el.nativeElement.style.backgroundColor = color;

  }

}

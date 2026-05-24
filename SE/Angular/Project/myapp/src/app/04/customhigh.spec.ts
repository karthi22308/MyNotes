import { ElementRef } from '@angular/core';
import { high } from './customhigh';

describe('Customhigh', () => {
  it('should create an instance', () => {
    const directive = new high();
    expect(directive).toBeTruthy();
  });
});

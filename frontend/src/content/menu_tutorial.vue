<template>
   <div class="textwrapper">
      <div class="row"> 
         <div class="eight columns">
         <h1 class="title">Welcome!</h1>
         <p>
            This brief tutorial describes the purpose of this tool, as well as some
            basic functionality.  You can re-open this tutorial at any time by
            pressing the question mark at the top of the page. 
         </p>

         <p class="note">
            Please read this tutorial before proceeding. It describes the purpose
            of the study, and the variables to be coded. 
         </p>

         <h1>Purpose of the study</h1>

         <p>
            The purpose of this tool is to collect and aggregate expert knowledge on
            the geographical distribution of conflict.
         </p>

         <h1>Variables</h1>

         <p>
            The data collected in this study are shapes drawn on a map. Each shape is
            associated with two variables. 
         </p>
         
         <p>
            The first variable is <span class="note">intensity</span>. This variable
            is meant to show the increase or decrease in conflict in a given area in
            the following year. 
         </p>
         
         <p>
            The intensity-variable ranges from -3 to 3. A score of -3 indicates a
            strong decrease in the conflict level in the coming year, and a score of
            3 indicates a strong increase in the conflict level in the comiing year.
         </p>

         <p>
            The second variable is <span class="note">confidence</span>. This
            variable expresses the confidence in the intensity prediction.
         </p>

         <p>
            The confidence-variable ranges from -3 to 3. A score of -3 indicates a
            strong confidence in the prediction, and a score of 3 indicates a weak
            confidence in the prediction.
         </p>
         </div>

         <div class="images four columns">
            <div class="imgwrapper">
               <img class="logoimage" :src="priologo" alt="">
            </div>
            <div class="imgwrapper">
               <img class="logoimage" :src="eulistcologo" alt="">
            </div>
         </div>
      </div>

      <div class="row">
         <div class="six columns">
            <h1>Choosing a project</h1>
            <p>
               There are five countries included in this study. Each is
               represented by a card on the menu screen. Click a card to
               display the corresponding map, and to start adding area-layers. 
            </p>

            <h1>Using the map</h1>

            <p>
               The areas are drawn on an interactive map. To draw on the map, you
               select the drawing tool from the top left on the screen, and click the
               map to place points. Draw points until you have enclosed the area of
               interest, and then click the first point you placed to finish the
               area.
            </p>

            <p>
               Each area is associated with a box located to the right of the map,
               with two sliders. The sliders let you enter values for the two
               variables, associating them with the area that is highlighted. To
               delete a drawn area, press the orange button in the associated box.
            </p>

            <p>
               Your data is saved in real time. You can revisit and revise each
               country-project by going back and forth between the menu and the map.
               When you are done, simply close the browser window.
            </p>
         </div>

         <div class="four columns">
            <img id="demogif" :src="demogif" alt="">
         </div>

      </div>

      <div class="row">
         <h1 class="title">Thank you for your contribution!</h1>
      </div>

      <div class="row">
         <h1>
            Til testerne:
         </h1>
         <p>
            Hei! Tusen takk for at dere har tatt dere tid til dette. Jeg er spent
            på hva dere synes. Med denne runden med testing er vi ute etter å
            finne ut hvordan det oppleves å bruke applikasjonen: Det er altså ikke
            så viktig hvor "riktige" dataene dere legger inn blir. Formålet med
            prosjektet denne applikasjonen er skrevet til er som nevnt å samle inn
            geografisk informasjon om konfliktrisiko, men formålet med testingen
            er bare å finne ut hvor lett applikasjonen er å bruke, og om det
            finnes noen skjulte bugs. 
         </p>

         <p>
            Bruk litt tid på å legge inn områder i de ulike landene. Hvis noe
            er uklart, sjekk denne hjelpesiden, men om det ikke står her er det
            viktig at jeg får vite hva dere lurer på! Prøv også gjerne å herje
            litt med de ulike funksjonene, og se om det lar seg gjøre å skape
            noe trøbbel for applikasjonen. 
         </p>

         <p>
            Det er kjent at applikasjonen kan "misse" data noen ganger, selv om
            jeg tror dette problemet har blitt løst nå. For å sjekke om dette
            skjer kan dere tegne inn noen områder, og så gå ut og inn av det
            samme landprosjektet og se om endringene deres ble registrert.
            Dette gjelder også for endringer i variabel-sliderene på siden.
         </p>
         <p>
            Det er helt supert om dere oppdager problemer med applikasjonen,
            for det betyr at vi får fikset problemene før den skal ut i "felt"!
            Derfor blir jeg veldig glad for å høre fra dere om dere opplever
            noe som er feil. Om dere har mulighet til det, la gjerne vinduet
            stå oppe og ta kontakt med meg (om dere vil fortsette å teste kan
            dere åpne en ny fane imens). Jeg kan nåes på epost
            (pglandsverk@gmail.com), og jeg sitter på kontoret i andre etasje
            mellom ni og fem. 
         </p>

         <p>
            Jeg tar også gjerne en prat med hver av dere når dere har fått
            testet litt, så jeg finner litt ut av hvordan det oppleves å bruke
            applikasjonen.
         </p>

         <p>
            Takk igjen! Mvh. Peder :)
         </p>
      </div>
   </div>
</template>

<script>
import priologo from "../images/priologo.png"
import eulistcologo from "../images/eulistcologo.png"
import demogif from "../images/testdrive.gif"

export default {
   data(){
      return {
         priologo: priologo,
         eulistcologo: eulistcologo,
         demogif: demogif, 
      }
   }
}

</script>

<style lang="sass"> 
   @import "../sass/variables.sass"

   .title   
      color: $ui_highlight
      font-size: 55px 

   .note
      display: inline-block
      color: $ui_highlight

   .images
      padding-top: 100px
      padding-right: 40px

   .logoimage
      max-height: 100%
      max-width: 100%
      text-align: center

   #demogif
      max-width: 150%

   .imgwrapper
      position: inline-block

   .row
      margin-right: 10px

</style>

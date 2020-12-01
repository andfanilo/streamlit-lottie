import {
  Streamlit,
  ComponentProps,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { useEffect, useRef } from "react"
import lottie, { AnimationItem } from "lottie-web"

interface PythonArgs {
  animationData: any
  loop: boolean | number
  speed: number
  direction: 1 | -1
  quality: "high" | "medium" | "low"
  height?: number
  width?: number
}

const StreamlitLottie = (props: ComponentProps) => {
  const lottieElementRef = useRef<HTMLDivElement>(null)
  const lottieInstanceRef = useRef<AnimationItem>()

  const {
    animationData,
    speed,
    direction,
    loop,
    quality,
    height,
    width,
  }: PythonArgs = props.args

  useEffect(() => {
    if (null === lottieElementRef.current) {
      return
    }

    lottieInstanceRef.current = lottie.loadAnimation({
      container: lottieElementRef.current,
      renderer: "svg",
      loop: loop,
      autoplay: true,
      animationData: animationData,
    })

    lottieInstanceRef.current.addEventListener("DOMLoaded", () => {
      Streamlit.setFrameHeight()
    })
    /*
    lottieInstanceRef.current.addEventListener("complete", () => {
      Streamlit.setComponentValue(true)
    })
    */

    return () => {
      if (!lottieInstanceRef.current) {
        return
      }
      lottieInstanceRef.current.removeEventListener("DOMLoaded")
      // lottieInstanceRef.current.removeEventListener("complete")
      lottieInstanceRef.current.destroy()
      lottieInstanceRef.current = undefined
    }
  }, [animationData, loop])

  useEffect(() => {
    if (!lottieInstanceRef.current) return
    lottie.setQuality(quality)
  }, [quality])

  useEffect(() => {
    if (!lottieInstanceRef.current) return
    if (Number.isNaN(speed)) return
    lottieInstanceRef.current.setSpeed(speed)
  }, [speed])

  useEffect(() => {
    if (!lottieInstanceRef.current) return
    lottieInstanceRef.current.setDirection(direction)
  }, [direction])

  return (
    <>
      <div
        style={{ width: width || "100%", height: height || "100%" }}
        ref={lottieElementRef}
      ></div>
      {console.log("Render")}
    </>
  )
}
export default withStreamlitConnection(StreamlitLottie)

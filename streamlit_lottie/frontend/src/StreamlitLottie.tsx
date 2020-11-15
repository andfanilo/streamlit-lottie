import {
  Streamlit,
  ComponentProps,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { useEffect, useRef } from "react"
import lottie, { AnimationItem } from "lottie-web"

interface PythonArgs {
  animationData: any
}

const StreamlitLottie = (props: ComponentProps) => {
  const lottieElementRef = useRef<HTMLDivElement>(null)
  const lottieInstanceRef = useRef<AnimationItem>()

  const { animationData }: PythonArgs = props.args

  useEffect(() => {
    if (null === lottieElementRef.current) {
      return
    }
    lottieInstanceRef.current = lottie.loadAnimation({
      container: lottieElementRef.current,
      renderer: "svg",
      loop: true,
      autoplay: true,
      animationData: animationData,
    })

    return () => {
      if (!lottieInstanceRef.current) {
        return
      }
      lottieInstanceRef.current.destroy()
      lottieInstanceRef.current = undefined
    }
  }, [animationData])

  useEffect(() => {
    Streamlit.setFrameHeight()
  })

  return <div style={{ width: 50, height: 50 }} ref={lottieElementRef}></div>
}
export default withStreamlitConnection(StreamlitLottie)
